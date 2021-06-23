//Maps the hash array to actual function names
//@author 
//@category -Restart-Service-
//@keybinding
//@menupath
//@toolbar

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.tuple.ImmutableTriple;
import org.apache.commons.lang3.tuple.Triple;

import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.util.exception.InvalidInputException;
import ghidra.util.exception.NotFoundException;

public class HashFuncStage2 extends HashFuncStage1 {
	protected String hash_array_symbol = "LOADED_FUNCS_UNK";
	protected int hash_array_length = 17;
	protected String key_symbol = "KEY";
	
	@Override
	protected List<Triple<Long, Long, Address>> collectDllHashes() throws NotFoundException {
		Address hash_array_address = getSymbolAddress(hash_array_symbol);
		Address key_address = getSymbolAddress(key_symbol);
		
		ArrayList<Triple<Long, Long, Address>> res = new ArrayList<Triple<Long, Long, Address>>();
		
		Listing l = currentProgram.getListing();
		
		Data k_dt = l.getDataAt(key_address);
		Data h_dt = l.getDataAt(hash_array_address);
		
		Long k;
		Long h;
		Address a;
		
		try {
			k = k_dt.getLong(0);
			h = h_dt.getLong(0);
			a = h_dt.getAddress();
		} catch (MemoryAccessException e) {
			printerr("Could not get key/hash: " + e.toString());
			return res;
		}
		
		for (int i = 0; i < hash_array_length; i++) {
			Triple<Long, Long, Address> t = new ImmutableTriple<Long, Long, Address>(h, k, a);
			res.add(t);
			
			h_dt = l.getDataAfter(a);
			try {
				h = h_dt.getLong(0);
				a = h_dt.getAddress();
			} catch (MemoryAccessException e) {
				printerr("Could not get key/hash: " + e.toString());
				return res;
			}
		}
		
		return res;
	}

	@Override
	protected void doStuffWithTripple(Triple<Long, Long, Address> p, String line) {
		try {
			createLabel(p.getRight(), line, true);
		} catch (Exception e) {
			printerr("Could not create label at " + p.getRight().toString());
		}

		printf("Set LABEL at: name: %s, dll_func_hash: %X, key: %X, ref: %s\n", line, p.getLeft(), p.getMiddle(), p.getRight().toString());
	}
}
