import sandbox_config


sandbox_config.onto = sandbox_config.Withable()
sandbox_config.onto.internal_holding = "moo"

import sandbox_needed.needed
f = sandbox_needed.needed.foo()
f.show()


