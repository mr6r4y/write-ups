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
import java.util.Arrays;
import java.util.List;

import org.apache.commons.lang3.tuple.Triple;
import org.apache.commons.lang3.tuple.ImmutableTriple;

import ghidra.app.emulator.EmulatorHelper;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.symbol.*;
import ghidra.util.Msg;
import ghidra.util.exception.CancelledException;
import ghidra.util.exception.NotFoundException;


public class EmuHashFunc extends GhidraScript {

	private String hash_func_name = "do_some_hash";
	private String load_dll_func_name = "dynamic_load_get_func";
	
	private long stack_offset = 0x000000002FFF0000L;
	private long stack_used = 0x10000L;
	private long str_offset = 0x0;
	
	private EmulatorHelper emu;
	private Address do_some_hash_addr;
	private List<Triple<Long, Long, Address>> dll_hashes;

	private Address getSymbolAddress(String symbolName) throws NotFoundException {
		Symbol symbol = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, symbolName,
			err -> Msg.error(this, err));
		if (symbol != null) {
			return symbol.getAddress();
		}
		throw new NotFoundException("Failed to locate label: " + symbolName);
	}
	
	private byte[] str2bytes(String str) {
		return (str + "\0").getBytes(Charset.forName("UTF-8"));
	}
	
	protected void emuInit() throws NotFoundException {
		Address current_stack = toAddr(stack_offset - stack_used);
		Address end_address = toAddr(0x00405b8);
		do_some_hash_addr = getSymbolAddress(hash_func_name);
		
		emu = new EmulatorHelper(currentProgram);
		
		emu.setBreakpoint(end_address);
		emu.writeRegister(emu.getStackPointerRegister(), current_stack.getOffset());
		emu.writeRegister("RBP", current_stack.getOffset());
		emu.writeRegister(emu.getPCRegister(), do_some_hash_addr.getOffset());
	}

	protected long doSomeHash(String str, long hash) {
		Address str_mem = toAddr(stack_offset - str_offset);
		byte[] str_bytes = str2bytes(str);
		println(Arrays.toString(str_bytes));
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

	protected boolean checkDllFuncName(String dll_name, String func_name, long dll_func_hash, long key) {
		String dll_name_lower = dll_name.toLowerCase();
		long dll_h = doSomeHash(dll_name_lower, key);
		long func_h = doSomeHash(func_name, key);
		
		return (dll_h ^ func_h) == dll_func_hash;
	}
	
	private Long getDllFuncHashFromCallRef(Reference ref) {
		// TO-DO: Implement backward propagation to references to data if any in RCX register
		return 0L;
	}
	
	private Long getKeyFromCallRef(Reference ref) {
		// TO-DO: Implement backward propagation to references to data if any in RDX register
		return 0L;
	}

	protected List<Triple<Long, Long, Address>> collectDllHashes() throws NotFoundException {
		Address f_addr = getSymbolAddress(load_dll_func_name);
		
		ArrayList<Triple<Long, Long, Address>> res = new ArrayList<Triple<Long, Long, Address>>();
		ReferenceManager r = currentProgram.getReferenceManager();
		ReferenceIterator references = r.getReferencesTo(f_addr);
		
		for(Reference ref: references) {
			Long h = getDllFuncHashFromCallRef(ref);
			Long k = getKeyFromCallRef(ref);
			Address a = ref.getFromAddress();
			Triple<Long, Long, Address> t = new ImmutableTriple<Long, Long, Address>(h, k, a);
			res.add(t);
		}
		
		return res;
	}

	@Override
	protected void run() throws Exception {
		File names_fl;

		try {
			names_fl = askFile("Supply a file with <dll-name>:<func-name> list to be checked", getCategory());
		} catch (CancelledException e) {
			return;
		}
		
		try {
			dll_hashes = collectDllHashes();
		} catch (NotFoundException e) {
			printerr(load_dll_func_name + "function symbol could not be found!");
			return;
		}
		
		try {
			emuInit();
		} catch (NotFoundException e) {
			printerr(hash_func_name + "function symbol could not be found!");
		}

		String line;
		FileReader nr = new FileReader(names_fl.getAbsolutePath());
		BufferedReader br = new BufferedReader(nr);
		while((line = br.readLine()) != null) {
			for(Triple<Long, Long, Address> p: dll_hashes) {
				String[] s = line.split(":");
				if(checkDllFuncName(s[0], s[1], p.getLeft(), p.getMiddle())) {
					printf("name: %s, dll_func_hash: %X, key: %X\n", line, p.getLeft(), p.getMiddle());
				}
			}
		}
		
		emu.dispose();
	}
	
}
