import sandbox_config

foo = None
gggg = sandbox_config.onto

with gggg:
    class Foo:
        def show(self):
            print(gggg.internal_holding)

    foo = Foo
