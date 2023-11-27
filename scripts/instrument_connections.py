import pyvisa

rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())

laser = rm.open_resource("ASRL7::INSTR")
laser.write_termination = '\r'
laser.read_termination = '\r'
laser.baud_rate = 9600
laser.data_bits = 8

response = laser.query('*IDN?', delay=1)
print(response)
laser.close()

powermeter = rm.open_resource('USB0::4883::32888::P0001012::0::INSTR')
powermeter.write_termination = '\r'
powermeter.read_termination = '\r'
print(powermeter.query('*IDN?'))
print(powermeter.query('*IDN?'))
