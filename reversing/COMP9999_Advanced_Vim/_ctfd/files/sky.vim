" Welcome to my Emulator! VimScript is super easy and intuitive to understand!
"
" There is no input validation so be careful :D
"
" To use this file, run the command:
"         vim -S sky.vim path/to/prog.sky

function! LogInit()
	call writefile([''], 'sky.log', 'b')
endfunction

function! LogLine(line)
	call writefile([a:line], 'sky.log', 'a')
endfunction

function! InitList(n)
	let tmp = []
	let i = 0
	while i < a:n
		let tmp = tmp + [0]
		let i = i + 1
	endwhile
	return tmp
endfunction

function! GetText()
	let text = []
	let i = 0
	while i < len(getline(1))
		let text += [str2nr(getline(1)[i:i+1], 16)]
		let i = i + 2
	endwhile
	return text
endfunction

function! SPInc(state, offset)
	let a:state['sp'] = (a:state['sp'] + a:offset) % 256
endfunction

function! PCInc(state, offset)
	let a:state['pc'] = (a:state['pc'] + a:offset) % 256
endfunction

function! EmuPushItem(state, item)
	call SPInc(a:state, -1)
	let sp = a:state['sp']
	let a:state['as'][sp] = a:item
endfunction

function! EmuPush(state)
	let pc = a:state['pc']
	let byte = a:state['text'][pc + 1]
	call PCInc(a:state, 1)

	call SPInc(a:state, -1)
	let sp = a:state['sp']
	let a:state['as'][sp] = byte
endfunction

function! EmuDup(state)
	let pc = a:state['pc']
	let offset = a:state['text'][pc + 1]
	call PCInc(a:state, 1)

	call SPInc(a:state, -1)
	let sp = a:state['sp']
	let a:state['as'][sp] = a:state['as'][sp+offset]
endfunction

function! EmuPop(state)
	let sp = a:state['sp']
	let value = a:state['as'][sp]
	call SPInc(a:state, 1)
	return value
endfunction

function! EmuLessThan(state)
	let a = EmuPop(a:state)
	let b = EmuPop(a:state)
	call EmuPushItem(a:state, a < b)
endfunction

function! EmuAdd(state)
	let a = EmuPop(a:state)
	let b = EmuPop(a:state)
	call EmuPushItem(a:state, a + b)
endfunction

function! EmuPeek(state)
	let addr = EmuPop(a:state)
	let item = a:state['as'][addr]
	call EmuPushItem(a:state, item)
endfunction

function! EmuPoke(state)
	let addr = EmuPop(a:state)
	let item = EmuPop(a:state)
	let a:state['as'][addr] = item
endfunction

function! EmuMod(state)
	let a = EmuPop(a:state)
	let b = EmuPop(a:state)
	call EmuPushItem(a:state, a % b)
endfunction

function! EmuXor(state)
	let a = EmuPop(a:state)
	let b = EmuPop(a:state)
	call EmuPushItem(a:state, xor(a, b))
endfunction

function! EmuIsZero(state)
	let tmp = EmuPop(a:state)
	call EmuPushItem(a:state, tmp == 0)
endfunction

function! EmuJumpCond(state)
	let offset = EmuPop(a:state)
	let cond = EmuPop(a:state)
	if cond != 0
		call PCInc(a:state, offset)
	endif
endfunction

function! EmuJump(state)
	let offset = EmuPop(a:state)
	call PCInc(a:state, offset)
endfunction

function! EmuSyscallExit(state)
	let a:state['finish'] = 1
endfunction

function! EmuSyscallLog(state)
	let length = EmuPop(a:state)
	let addr = EmuPop(a:state)

	let tmp = a:state['as'][addr:addr+length-1]
	let tmp = map(tmp, {_, val -> nr2char(val)})
	let tmp = join(tmp, '')
	call LogLine(tmp)
endfunction

function! EmuPopStr(state, length)
	let sp = a:state['sp']
	let tmp = a:state['as'][sp:sp+a:length-1]
	let tmp = map(tmp, {_, val -> nr2char(val)})
	let tmp = join(tmp, '')
	call SPInc(a:state, a:length)
	return tmp
endfunction

function! EmuMemcpy(state)
	let addr = EmuPop(a:state)
	let length = EmuPop(a:state)
	let i = 0
	while i < length
		let a:state['as'][addr+i] = EmuPop(a:state)
		let i += 1
	endwhile
endfunction

function! EmuSyscallConnect(state)

	let length = EmuPop(a:state)
	let path = EmuPopStr(a:state, length)

	let channel = ch_open(path)
	if ch_status(channel) != 'open'
		let a:state['finish'] = 1
		return
	endif

	call EmuPushItem(a:state, channel)
endfunction

function! EmuSyscallRead(state)
	let addr = EmuPop(a:state)
	let length = EmuPop(a:state)
	let buf = EmuPop(a:state)
	let channel = a:state['as'][addr]

	let data = ch_read(channel)[1]
	if len(data) != length
		let a:state['finish'] = 1
		return
	endif

	let i = 0
	while i < length
		let a:state['as'][buf + i] = char2nr(data[i])
		let i += 1
	endwhile

endfunction

function! EmuSyscallSend(state)
	let addr = EmuPop(a:state)
	let length = EmuPop(a:state)
	let data = EmuPopStr(a:state, length)
	let channel = a:state['as'][addr]
	call ch_sendexpr(channel, data)
endfunction

function! EmuSyscallClose(state)
	let addr = EmuPop(a:state)
	let channel = a:state['as'][addr]
	call ch_close(channel)
endfunction

function! EmuSyscall(state)
	let sysnum = EmuPop(a:state)

	if sysnum == 0x00
		call EmuSyscallExit(a:state)
	elseif sysnum == 0x01
		call EmuSyscallLog(a:state)
	elseif sysnum == 0x02
		call EmuSyscallConnect(a:state)
	elseif sysnum == 0x03
		call EmuSyscallRead(a:state)
	elseif sysnum == 0x04
		call EmuSyscallSend(a:state)
	elseif sysnum == 0x05
		call EmuSyscallClose(a:state)
	endif

endfunction

function! SkyEmulator()

	call LogInit()

	let state = {'text': GetText(), 'pc': 0, 'sp': 256, 'as': InitList(256), 'finish': 0}

	while (state['finish'] == 0) && (state['pc'] < len(state['text']))
		let pc = state['pc']
		let opcode = state['text'][pc]

		if opcode == 0x92
			call EmuPush(state)
		elseif opcode == 0x6b
			call EmuPop(state)
		elseif opcode == 0x5f
			call EmuSyscall(state)
		elseif opcode == 0x0f
			call EmuDup(state)
		elseif opcode == 0x82
			call EmuMemcpy(state)
		elseif opcode == 0x08
			call EmuLessThan(state)
		elseif opcode == 0xb8
			call EmuJumpCond(state)
		elseif opcode == 0x34
			call EmuJump(state)
		elseif opcode == 0x67
			call EmuAdd(state)
		elseif opcode == 0x07
			call EmuPeek(state)
		elseif opcode == 0x6e
			call EmuPoke(state)
		elseif opcode == 0xc3
			call EmuMod(state)
		elseif opcode == 0xbb
			call EmuXor(state)
		elseif opcode == 0xd8
			call EmuIsZero(state)
		else
			let state['finish'] = 1
		endif

		let state['pc'] += 1

	endwhile

endfunction

call SkyEmulator()
