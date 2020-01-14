import utils as u

ic_org=u.get_input('day25.txt').split(',')
ic_org=[int(x) for x in ic_org]
vm=u.Acii(ic_org.copy())
print("You can pick items up with 'take'. Drop them with 'drop' and list items with 'inv'.")


done=False
while not done:
    out=vm.update()
    if out[-1]==99:
        done=True
        print('game over')
    print(u.ascii_to_txt(out))
    if out==[67, 111, 109, 109, 97, 110, 100, 63, 10]:
        inn=[ord(x) for x in input()]+[10]
        vm.addqueue(inn)
        if inn==[114, 101, 115, 101, 116, 10]:
            break

