-- comment is here

function factorial(n)
  if n == 0 then
    return 1
  else
    return n * factorial(n - 1)
  end
end


i = 0
a = factorial(i)
while a < 1000 do
i = i + 1
a = factorial(i)
end



print("First factorial greater than 1000 is factorial(" + tostring(i) + ") = " + tostring(a))
