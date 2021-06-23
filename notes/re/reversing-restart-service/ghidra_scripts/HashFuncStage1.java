//Emulate hash string checks for getting the DLL calls
//@author mr6r4y
//@category -Restart-Service-
//@keybinding
//@menupath
//@toolbar

import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.tuple.Triple;
import org.apache.commons.lang3.tuple.ImmutableTriple;

import ghidra.app.emulator.EmulatorHelper;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.lang.Register;
import ghidra.program.model.listing.CodeUnit;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.symbol.*;
import ghidra.util.Msg;
import ghidra.util.exception.CancelledException;
import ghidra.util.exception.NotFoundException;


public class HashFuncStage1 extends GhidraScript {

	protected String hash_func_name = "do_some_hash";
	protected String load_dll_func_name = "dynamic_load_get_func";
	
	protected long stack_offset = 0x000000002FFF0000L;
	protected long stack_used = 0x10000L;
	protected long str_offset = 0x0;
	protected long current_stack = stack_offset - stack_used;
	protected long end_address_offset = 0x00405b8;
	
	protected EmulatorHelper emu;
	protected Address do_some_hash_addr;
	protected List<Triple<Long, Long, Address>> dll_hashes;

	protected Address getSymbolAddress(String symbolName) throws NotFoundException {
		Symbol symbol = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, symbolName,
			err -> Msg.error(this, err));
		if (symbol != null) {
			return symbol.getAddress();
		}
		throw new NotFoundException("Failed to locate label: " + symbolName);
	}
	
	protected byte[] str2bytes(String str) {
		return (str + "\0").getBytes(Charset.forName("UTF-8"));
	}
	
	protected void emuInit() throws NotFoundException {
		do_some_hash_addr = getSymbolAddress(hash_func_name);
		emu = new EmulatorHelper(currentProgram);
		
		emu.setBreakpoint(toAddr(end_address_offset));
	}

	protected long doSomeHash(String str, long hash) {
		emu.writeRegister(emu.getStackPointerRegister(), current_stack);
		emu.writeRegister("RBP", current_stack);
		emu.writeRegister(emu.getPCRegister(), do_some_hash_addr.getOffset());
		
		Address str_mem = toAddr(stack_offset - str_offset);
		byte[] str_bytes = str2bytes(str);
		emu.writeMemory(str_mem,  str_bytes);
		
		emu.writeRegister("RCX", str_mem.getOffset());
		emu.writeRegister("RDX", hash);
		
		try {
			emu.run(monitor);
		} catch (CancelledException e) {
			return 0L;
		}

		Long rax = emu.readRegister("RAX").longValue();

		return rax;
	}

	protected Long calckDllFuncNameHash(String dll_name, String func_name, long key) {
		String dll_name_lower = dll_name.toLowerCase();
		long dll_h = doSomeHash(dll_name_lower, key);
		long func_h = doSomeHash(func_name, key);
//		printf("dll: %s, func: %s, dll_func_hash: %X, key: %X\n", dll_name_lower, func_name, dll_h ^ func_h, key);
		return (dll_h ^ func_h);
	}
	
	protected Long getRegRefFromCallAddr(Address call_addr, Listing l, String reg_name) {
		Instruction ins = l.getInstructionBefore(call_addr);
		for(byte i = 5; i > 0; i--) {
			Object[] op_ar = ins.getOpObjects(0);
			if (op_ar.length == 1) {
				if (op_ar[0] instanceof Register) {
					Register op = (Register) op_ar[0];
					if (op.getName().compareTo(reg_name) == 0) {
						for (Reference ref: ins.getReferencesFrom()) {
							try {
								return getLong(ref.getToAddress());
							} catch (MemoryAccessException e) {}
						}
					}
				}
			}
			ins = ins.getPrevious();
		}
		
		return 0L;
	}
	
	protected Long getDllFuncHashFromCallAddr(Address call_addr, Listing l) {
		return getRegRefFromCallAddr(call_addr, l, "RDX");
	}

	protected Long getKeyFromCallAddr(Address call_addr, Listing l) {
		return getRegRefFromCallAddr(call_addr, l, "R8");
	}

	protected List<Triple<Long, Long, Address>> collectDllHashes() throws NotFoundException {
		Address f_addr = getSymbolAddress(load_dll_func_name);
		
		ArrayList<Triple<Long, Long, Address>> res = new ArrayList<Triple<Long, Long, Address>>();
		ReferenceManager r = currentProgram.getReferenceManager();
		ReferenceIterator references = r.getReferencesTo(f_addr);
		
		Listing l = currentProgram.getListing();
		
		for(Reference ref: references) {
			Address a = ref.getFromAddress();
			Long h = getDllFuncHashFromCallAddr(a, l);
			Long k = getKeyFromCallAddr(a, l);
			if (k != 0 && h != 0) {
				Triple<Long, Long, Address> t = new ImmutableTriple<Long, Long, Address>(h, k, a);
				res.add(t);
			}
		}
		
		return res;
	}
	
	protected void doStuffWithTripple(Triple<Long, Long, Address> p, String line) {
		Listing listing = currentProgram.getListing();
		listing.setComment(p.getRight(), CodeUnit.EOL_COMMENT, line);
		printf("Set comment for name: %s, dll_func_hash: %X, key: %X, ref: %s\n", line, p.getLeft(), p.getMiddle(), p.getRight().toString());
	}

	@Override
	protected void run() throws Exception {
		File names_fl;

		try {
			names_fl = askFile("Supply a file with <dll-name>:<func-name> list to be checked", "Check");
		} catch (CancelledException e) {
			return;
		}
		
		try {
			dll_hashes = collectDllHashes();
		} catch (NotFoundException e) {
			printerr(load_dll_func_name + "function symbol could not be found!");
			return;
		}
		
		println("--------- Refs ---------");
		for(Triple<Long, Long, Address> p: dll_hashes) {
			printf("address: %s, dll_func_hash: %X, key: %X\n", p.getRight(), p.getLeft(), p.getMiddle());
		}
		println("------------------------");
		
		try {
			emuInit();
		} catch (NotFoundException e) {
			printerr(hash_func_name + "function symbol could not be found!");
		}

		String line;
		FileReader nr = new FileReader(names_fl.getAbsolutePath());
		BufferedReader br = new BufferedReader(nr);
		
		while((line = br.readLine()) != null) {
			String[] s = line.split(":");
			Long current_hash = 0L;
			Long last_key = 0L;
			for(Triple<Long, Long, Address> p: dll_hashes) {
				if ((p.getMiddle().compareTo(last_key) != 0) || (current_hash.equals(0L))) {
					last_key = p.getMiddle();
					current_hash = calckDllFuncNameHash(s[0], s[1], last_key);
				}
				
				if (current_hash.equals(p.getLeft())) {
					doStuffWithTripple(p, line);
				}
				
				if (monitor.isCancelled()) {
					br.close();
					emu.dispose();
					return;
				}
			}
		}
		
		emu.dispose();
	}
	
}
