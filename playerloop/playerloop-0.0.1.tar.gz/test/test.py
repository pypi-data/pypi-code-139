from playerloop import PlayerLoop

key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbklkIjo4MDQzNzM2N30.MGgRGayX_lTA70Hx3wxEflB8RbnfZxkCJega27EkOXU'

pl = PlayerLoop(key, 'test_app')
pl.send_report('test report please ignore')
