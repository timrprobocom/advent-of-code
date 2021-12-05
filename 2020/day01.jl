using DelimitedFiles

test = [
1721,
979,
366,
299,
675,
1456
]

live = readdlm("day01.txt",Int32)

function pass1(data)
    for (i,d0) in enumerate(data)
        for d1 in data[i+1:end]
            if d0+d1 == 2020
                return d0*d1
             end
        end
    end
end

function pass2(data)
    for (i,d0) in enumerate(data)
        for (j,d1) in enumerate(data[i+1:end])
            for d2 in data[i+j+1:end]
                if d0+d1+d2 == 2020
                    return d0*d1*d2
                end
            end
        end
    end
end

println( pass1(test) )
println( pass2(test) )
println( "Pass 1:", pass1(live) )
println( "Pass 2:", pass2(live) )
