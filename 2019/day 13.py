with open('input13.txt') as file:
    data = [*map(int, file.read().split(','))]

class Executer:
    def __init__(self, array, inputs=[]):
        self.array = [*array]+[0]*1000
        self.inputs = inputs

    def execute(self):
        instr = self.array
        pointer = 0
        relative_base = 0
        while True:
            to_exec = instr[pointer]
            if to_exec == 99:
                break

            temp = str(to_exec)
            opcode =  to_exec if len(temp) < 2 else int(temp[-2:])
            parameter_1 = 0 if len(temp) < 3 else int(temp[-3])
            parameter_2 = 0 if len(temp) < 4 else int(temp[-4])
            parameter_3 = 0 if len(temp) < 5 else int(temp[-5])

            p1 = (instr[pointer+1], pointer+1, relative_base+instr[pointer+1])[parameter_1]
            if opcode == 3:
                instr[p1] = self.inputs[0]
                del self.inputs[0]
                pointer += 2
            elif opcode == 4:
                yield instr[p1]
                pointer += 2
            elif opcode == 9:
                relative_base += instr[p1]
                pointer += 2
            else:
                p2 = (instr[pointer+2], pointer+2, relative_base+instr[pointer+2])[parameter_2]
                if opcode == 5:
                    if instr[p1] != 0:
                        pointer = instr[p2]
                    else:
                        pointer += 3
                elif opcode == 6:
                    if instr[p1] == 0:
                        pointer = instr[p2]
                    else:
                        pointer += 3
                else:
                    p3 = (instr[pointer+3], pointer+3, relative_base+instr[pointer+3])[parameter_3]
                    if opcode == 1:
                        instr[p3] = instr[p1] + instr[p2]
                    elif opcode == 2:
                        instr[p3] = instr[p1] * instr[p2]
                    elif opcode == 7:
                        instr[p3] = 1 if instr[p1] < instr[p2] else 0
                    elif opcode == 8:
                        instr[p3] = 1 if instr[p1] == instr[p2] else 0
                    pointer += 4

#soluzione 1
g1 = Executer(data).execute()
tiles1 = dict()
for x in g1:
    y = next(g1)
    id = next(g1)
    tiles1[(x, y)] = id

print(sum(1 for i in tiles1.values() if i == 2))

#soluzione 2 (è veramente brutta ma funziona efficientemente)
new_game = Executer([2]+data[1:])
g2 = new_game.execute()
new_game.ball_pos = new_game.paddle_pos = 0
tiles2 = dict()
for x in g2:
    y = next(g2)
    id = next(g2)
    if x == -1 and y == 0:
        score = id
        continue
    tiles2[(x, y)] = id
    if id == 3:
        new_game.paddle_pos = x
    elif id == 4:
        new_game.ball_pos = x
        if new_game.ball_pos - new_game.paddle_pos == 0:
            new_game.inputs.append(0)
        else:
            new_game.inputs.append(1 if new_game.ball_pos > new_game.paddle_pos else -1)

print(score)