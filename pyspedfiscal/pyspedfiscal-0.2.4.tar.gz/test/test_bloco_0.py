from datetime import date
from decimal import Decimal
from pyspedfiscal.bloco_0 import Bloco0
import unittest


class TestBloco0(unittest.TestCase):

    def setUp(self) -> None:

        bloco = """
|0000|016|0|01072022|31072022|EMPRESA TESTE|14028298000152||SP|009371438460|3550308|||A|0|
|0001|0|
|0002|00|
|0005|EMPRESA TESTE|25821270|RUA EMPRESA TESTE|1111||BAIRRO EMPRESA TESTE|2499999999|||
|0100|CONTADOR TESTE|25142702000|1-SP-111111/O-1||25805290|RUA CONTADOR|111|ENDERECO CONTADOR|BAIRRO CONTADOR|2499999999||emailcontador@contador.com.br|3550308|
|0150|1|FORNECEDOR 1|1058|03446003000141|||3301702||ENDERECO FORNECEDOR 1|1111||BAIRRO FORNECEDOR 1|
|0150|2|FORNECEDOR 2|1058|97509345000107|||3550308||ENDERECO FORNECEDOR 1|2222||BAIRRO FORNECEDOR 2|
|0150|3|FORNECEDOR 3|1058|05929208000103|||3550308||ENDERECO FORNECEDOR 1|3333||BAIRRO FORNECEDOR 3|
|0150|4|FORNECEDOR 4|1058|13992567000133|||3550308||ENDERECO FORNECEDOR 1|4444||BAIRRO FORNECEDOR 4|
|0150|5|FORNECEDOR 5|1058|38284654000167|||3550308||ENDERECO FORNECEDOR 1|5555||BAIRRO FORNECEDOR 5|
|0190|KG|KILO|
|0190|UN|UNIDADE|
|0200|1|PRODUTO 1|||UN|00|27101921||||||
|0200|2|PRODUTO 2|||KG|00|27101921||||||
|0200|3|PRODUTO 3|||KG|00|27101921||||||
|0200|4|PRODUTO 4|||KG|00|27101921||||||
|0200|5|PRODUTO 5|||KG|00|27101921||||||
|0400|1653002|Natureza Teste|
|0450|1|Informacaoo Complementar Teste|
|0460|1|Observacao Teste|
|0990|21|""".splitlines()

        self.bloco_0 = Bloco0.ler_registros(bloco)

    def test_deve_ler_um_registro_0000(self):
        registro_0000 = self.bloco_0.registro_0000

        reg = registro_0000.reg
        dt_ini = registro_0000.dt_ini
        dt_fin = registro_0000.dt_fin

        self.assertEqual(reg, '0000')
        self.assertEqual(dt_ini, date(2022, 7, 1))
        self.assertEqual(dt_fin, date(2022, 7, 31))

    def test_deve_ler_um_registro_0001(self):
        registro_0001 = self.bloco_0.registro_0001

        reg = registro_0001.reg
        ind_mov = registro_0001.ind_mov

        # |0001|0|

        self.assertEqual(reg, '0001')
        self.assertEqual(ind_mov, '0')

    def test_deve_ler_um_registro_0200(self):
        registro_0200 = self.bloco_0.registro_0001.registros_0200[1]

        # |0200|2|PRODUTO 2|||KG|00|27101921||||||

        self.assertEqual(registro_0200.reg, '0200')
        self.assertEqual(registro_0200.cod_item, '2')
        self.assertEqual(registro_0200.descr_item, 'PRODUTO 2')
        self.assertEqual(registro_0200.cod_barra, None)
        self.assertEqual(registro_0200.cod_ant_item, None)
        self.assertEqual(registro_0200.unid_inv, 'KG')
        self.assertEqual(registro_0200.tipo_item, '00')
        self.assertEqual(registro_0200.cod_ncm, '27101921')
        self.assertEqual(registro_0200.ex_ipi, None)
        self.assertEqual(registro_0200.cod_gen, None)
        self.assertEqual(registro_0200.cod_lst, None)
        self.assertEqual(registro_0200.aliq_icms, None)
        self.assertEqual(registro_0200.cest, None)

    def test_deve_ler_um_registro_0460(self):
        registro_0460 = self.bloco_0.registro_0001.registros_0460[0]

        # |0460|1|Observacao Teste|

        self.assertEqual(registro_0460.reg, '0460')
        self.assertEqual(registro_0460.cod_obs, '1')
        self.assertEqual(registro_0460.txt, 'Observacao Teste')


if __name__ == '__main__':
    unittest.main()
