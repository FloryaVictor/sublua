print("Enter a:")
a = tonumber(read())
print("Enter b:")
b = tonumber(read())
print("Enter op(+, -, *, /):")
op = read()

if op == "+" then
    result = a + b
else
    if op == "-" then 
        result = a - b
    else
        if op == "*" then 
            result = a * b
        else
            if op == "/" then 
                result = a / b
            end
        end
    end
end


print(result)