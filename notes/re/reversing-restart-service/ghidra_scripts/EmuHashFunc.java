//Emulate hash string checks for getting the DLL calls
//@author mr6r4y
//@category -Restart-Service-
//@keybinding
//@menupath
//@toolbar

import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.math.BigInteger;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import generic.stl.Pair;
import ghidra.app.emulator.EmulatorHelper;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.symbol.*;
import ghidra.util.Msg;
import ghidra.util.exception.CancelledException;
import ghidra.util.exception.NotFoundException;
import ghidra.program.model.symbol.SymbolUtilities;


public class EmuHashFunc extends GhidraScript {

	private EmulatorHelper emu;
	private Address do_some_hash_addr;
	private long stack_offset = 0x000000002FFF0000L;
	private long stack_used = 0x10000L;
	private long str_offset = 0x0;
	private List<Pair<BigInteger, BigInteger>> dll_hashes;

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
		do_some_hash_addr = getSymbolAddress("do_some_hash");
		
		emu = new EmulatorHelper(currentProgram);
		
		emu.setBreakpoint(end_address);
		emu.writeRegister(emu.getStackPointerRegister(), current_stack.getOffset());
		emu.writeRegister("RBP", current_stack.getOffset());
		emu.writeRegister(emu.getPCRegister(), do_some_hash_addr.getOffset());
	}

	protected BigInteger doSomeHash(String str, long hash) {
		Address str_mem = toAddr(stack_offset - str_offset);
		byte[] str_bytes = str2bytes(str);
		println(Arrays.toString(str_bytes));
		emu.writeMemory(str_mem,  str_bytes);
		
		emu.writeRegister("RCX", str_mem.getOffset());
		emu.writeRegister("RDX", hash);
		
		try {
			emu.run(monitor);
		} catch (CancelledException e) {
			return BigInteger.ZERO;
		}
		
		BigInteger rax = emu.readRegister("RAX");
		
		return rax;
	}
	
	protected boolean checkDllFuncName(String dll_name, String func_name, BigInteger dll_func_hash, BigInteger key) {
		// TO-DO: Implement the DLL-func check
		return false;
	}

	protected List<Pair<BigInteger, BigInteger>> collectDllHashes() {
		// TO-DO: Gather all the <dll_func_hash>:<key> from the program itself
		return new ArrayList<Pair<BigInteger, BigInteger>>();
	}
	
	@Override
	protected void run() throws Exception {
		File names_fl;
		
		try {
			emuInit();
		}catch (NotFoundException e) {
			printerr("Hash function symbol could not be found!");
		}

		try {
			names_fl = askFile("Supply a file with <dll-name>:<func-name> list to be checked", getCategory());
		}catch (CancelledException e) {
			return;
		}
		
		dll_hashes = collectDllHashes();

		String line;
		FileReader nr = new FileReader(names_fl.getAbsolutePath());
		BufferedReader br = new BufferedReader(nr);
		while((line = br.readLine()) != null) {
			for(Pair<BigInteger, BigInteger> p: dll_hashes) {
				String[] s = line.split(":");
				if(checkDllFuncName(s[0], s[1], p.first, p.second)) {
					printf("name: %s, dll_func_hash: %X, key: %X\n", line, p.first, p.second);
				}
			}
		}
		
		
//		BigInteger a = doSomeHash("kernel32.dll", 0x406E72A20F0BE37DL);
//		printf("a=%X\n", a);
		emu.dispose();
	}
	
}
