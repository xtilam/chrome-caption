local scan1List = {}

function scanOne()
    local text = "This is content"
    local hexLength = string.format(' %02X', text:len())
    local textScan = (text):toScanUTF8()
    
    local resultScan = AOBScan(textScan)
    scan1List = {}

    if not resultScan then
        return writeResult(0)
    end
    
    local result = ""
    local start = ""
    local address = nil

    for i = 0, resultScan.Count - 1 do
        address = resultScan[i]
        local subScan = AOBScan(address:byteArrayFromHex() .. hexLength)

        if subScan then
            for j = 0, subScan.Count - 1 do
                -- print('find address', subScan[j])
                table.insert(scan1List, subScan[j])
            end
        end
    end

    writeResult(#scan1List)
end

function scanTwo()
    local text = "I live in a house near mountains"

    local textLength = text:len() * 2
    if not #scan1List then
        return writeResult(0)
    end 

    for i, address in pairs(scan1List) do
        local pointer = readPointer(address)
        if pointer then
            if readString(pointer, textLength, true) == text then
                return writeResult(tonumber(address, 16))
            end
        end
    end

    return writeResult(0)
end

function string.fromhex(str)
    return (str:gsub('..', function(cc)
        return string.char(tonumber(cc, 16))
    end))
end

function string.byteArrayFromHex(str, length)
    length = length or 8
    local strByte = ''
    local currentNum = tonumber(str, 16)

    for i = 1, length do
        local num = currentNum % 256
        currentNum = math.floor(currentNum / 256)
        strByte = strByte .. string.format('%02X', num) .. ' '
    end
 
    return strByte
end

function string.toScanUTF8(str)
    return (str:gsub('.', function(c)
        return string.format('%02X', string.byte(c)) .. ' 00 '
    end))
end

function string.toScan(str)
    return (str:gsub('.', function(c)
        return string.format('%02X', string.byte(c)) .. ' '
    end))
end