function writeFile(path, data)
    local f = io.open(path, "w")

    if f == nil then
        return
    end

    f:write(data)
    f:close()
end

function writeResult(data)
    writeFile(ceResultPath, data)
end

-- function scanByteArray(byte)
--     local resultScan = AOBScan(byte)
--     if not resultScan then
--         return writeResult('')
--     end

--     local result = ""
--     local start = ""

--     for i = 0, resultScan.Count - 1 do
--         result = result .. start .. address
--         start = "\n"
--     end

--     writeResult(result)
-- end
