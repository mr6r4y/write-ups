//Stage-3 patch and decrypt payload.
//
//Decrypt code:
//
//  if (dst[0x8d] == 3) {
//    do_some_decrypt((uint *)(dst + 1),dst + 5,dst + 0x90,*dst + -0x240);
//    LoadLibraryA = do_some_hash((char *)(dst + 0x1fc),*(undefined8 *)(dst + 10));
//    if (LoadLibraryA != *(longlong *)(dst + 0x23c)) goto LAB_00404b70;
//  }
//@author mr6r4y
//@category -Restart-Service-
//@keybinding
//@menupath
//@toolbar

import java.math.BigInteger;

import ghidra.app.emulator.EmulatorHelper;
import ghidra.app.script.GhidraScript;
import ghidra.framework.store.LockException;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressOverflowException;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.mem.MemoryConflictException;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolUtilities;
import ghidra.util.Msg;
import ghidra.util.exception.CancelledException;
import ghidra.util.exception.DuplicateNameException;
import ghidra.util.exception.NotFoundException;
import ghidra.util.LittleEndianDataConverter;


public class PayloadDecodeStage3 extends GhidraScript {
	
	private String start_label = "START_ST3_DECRYPT";
	private String end_label = "END_ST3_DECRYPT";
	private String shellcode_memblock_name = "shellcode_stage_3";
	
	private String shellcode_start_lable = "SHELLCODE_BASE";	
	private Integer shellcode_size = 0x1CBF;
	
	private Long alloc_mem_offset = 0x60000000L;
	private Integer alloc_mem_size = shellcode_size;
	
	private long stack_offset = 0x2FFF0000L;
	private long stack_used = 0x10000L;
	private long current_stack = stack_offset - stack_used;
	
	
	private EmulatorHelper emu;
	
	private Address getSymbolAddress(String symbolName) throws NotFoundException {
		Symbol symbol = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, symbolName,
			err -> Msg.error(this, err));
		if (symbol != null) {
			return symbol.getAddress();
		}
		throw new NotFoundException("Failed to locate label: " + symbolName);
	}
	
	private void setEmuMemory() throws NotFoundException, MemoryAccessException {
		Address shcAddr = getSymbolAddress(shellcode_start_lable);
		Memory mem = currentProgram.getMemory();
		byte[] shc = new byte[shellcode_size];
		mem.getBytes(shcAddr, shc);
		
		emu.writeMemory(toAddr(alloc_mem_offset), shc);
	}
	
	private boolean decrypt_shellcode_st3() throws NotFoundException, MemoryAccessException {
		emu = new EmulatorHelper(currentProgram);

		emu.writeRegister(emu.getPCRegister(), getSymbolAddress(start_label).getOffset());
		emu.setBreakpoint(getSymbolAddress(end_label));

		emu.writeRegister(emu.getStackPointerRegister(), current_stack);

		setEmuMemory();

		emu.writeRegister("RSI", alloc_mem_offset);

		try {
			emu.run(monitor);
		} catch (CancelledException e) {
			printerr("Emulation canceled !");
			emu.dispose();
			return false;
		}

		try {
			emu.createMemoryBlockFromMemoryState(shellcode_memblock_name, toAddr(alloc_mem_offset), alloc_mem_size, false, monitor);
		} catch (MemoryConflictException | AddressOverflowException | CancelledException | LockException
				| DuplicateNameException e) {
			printerr("Could not export shellcode to a memory block: " + e.toString());
		}
		
		BigInteger rax = BigInteger.valueOf(emu.readRegister("RAX").longValue());
		BigInteger rsi = BigInteger.valueOf(emu.readRegister("RSI").longValue());
		
		printf("RAX = 0x%X\n", rax);
		printf("RSI = 0x%X\n", rsi);
		
		byte[] hashBytes = emu.readMemory(toAddr(rsi.longValue() + 0x8f0L), 8);
		BigInteger hash = LittleEndianDataConverter.INSTANCE.getBigInteger(hashBytes, 8, false);
		
		printf("hash = 0x%X\n", hash.longValue());

		emu.dispose();
		
		return hash.equals(rax);
	}

	@Override
	protected void run() throws Exception {
		boolean success = decrypt_shellcode_st3();
		if (success) {
			println("SUCCESS !");
		} else {
			printerr("FAILURE !");
		}
	}
}
