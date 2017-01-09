import enum
from itertools import product


class bools(enum.Enum):
    true = 1
    false = 0


class gate:
    rules = {}

    def __call__(self, *r):
        return self.rules.get(tuple(i for i in r))  #py3.4pls


class or_gate(gate):
    rules = {
        (bools.false, bools.false): bools.false,
        (bools.false, bools.true): bools.true,
        (bools.true, bools.false): bools.true,
        (bools.true, bools.true): bools.true
    }


class and_gate(gate):
    rules = {
        (bools.false, bools.false): bools.false,
        (bools.false, bools.true): bools.false,
        (bools.true, bools.false): bools.false,
        (bools.true, bools.true): bools.true
    }


class xor_gate(gate):
    rules = {
        (bools.false, bools.false): bools.false,
        (bools.false, bools.true): bools.true,
        (bools.true, bools.false): bools.true,
        (bools.true, bools.true): bools.false
    }


class not_gate(gate):
    rules = {(bools.false): bools.true, (bools.true): bools.false}


class nand_gate(gate):
    rules = {
        (bools.false, bools.false): bools.true,
        (bools.false, bools.true): bools.true,
        (bools.true, bools.false): bools.true,
        (bools.true, bools.true): bools.false
    }


class nor_gate(gate):
    rules = {
        (bools.false, bools.false): bools.true,
        (bools.false, bools.true): bools.false,
        (bools.true, bools.false): bools.false,
        (bools.true, bools.true): bools.false
    }


class inp_out_src:
    def __init__(self):
        self.outputs = []
        self.inputs = []

    def add_output(self, output):
        self.outputs.append(output)

    def add_input(self, input_):
        self.inputs.append(input_)


class connection:
    def __init__(self, from_, to):
        self.from_ = from_
        from_.add_output(self)
        self.to = to
        to.add_input(self)
        self.val = bools.false

    def receive(self, val):
        self.val = val
        self.to.update()

    def __bool__(self):
        return self.val == bools.true


class active_gate(inp_out_src):
    def __init__(self, gate):
        super().__init__()
        self.gate = gate()

    def update(self):
        for i in self.outputs:
            i.receive(self.gate(*(k.val for k in self.inputs)))


class static_value(inp_out_src):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def update(self):
        for i in self.outputs:
            i.receive(self.val)

    def set(self, value):
        self.val = value
        self.update()


class output(inp_out_src):
    def __init__(self):
        super().__init__()
        self.val = bools.false

    def update(self):
        self.val = bools.true if any((i.val.value
                                      for i in self.inputs)) else bools.false


if __name__ == "__main__":
    xor = active_gate(xor_gate)
    and_ = active_gate(and_gate)

    x = static_value(bools.false)
    y = static_value(bools.true)

    out_s = output()
    out_c = output()

    x_to_xor = connection(x, xor)
    y_to_xor = connection(y, xor)

    x_to_and = connection(x, and_)
    y_to_and = connection(y, and_)

    xor_to_out_s = connection(xor, out_s)
    and_to_out_c = connection(and_, out_c)

    combs = product([bools.false, bools.true], repeat=2)

    for x_, y_ in combs:
        x.set(x_)
        y.set(y_)
        print("x:{}, y:{}, s:{}, c:{}".format(
            x.val.value, y.val.value, out_s.val.value, out_c.val.value))
