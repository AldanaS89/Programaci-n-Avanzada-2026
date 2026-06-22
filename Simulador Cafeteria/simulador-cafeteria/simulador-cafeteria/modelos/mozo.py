"""
Mozo: empleado que toma pedidos durante la jornada.

Demuestra:
- ENCAPSULAMIENTO: la clave se guarda HASHEADA (SHA-256) en un atributo
  "privado" (doble guion bajo). Nunca se almacena ni se expone en texto plano;
  solo se puede verificar comparando hashes.
- AGREGACIÓN: un Mozo agrupa sus Pedidos (los pedidos existen de forma
  independiente; el mozo los referencia).
"""
import hashlib


class Mozo:
    def __init__(self, nombre, clave):
        self.nombre = nombre
        self.__clave_hash = self._hashear(clave)   # privado: nunca en texto plano
        self._pedidos = []                          # pedidos atendidos por este mozo

    @staticmethod
    def _hashear(clave):
        return hashlib.sha256(clave.encode()).hexdigest()

    def verificar_clave(self, clave_ingresada):
        """Compara el hash de lo ingresado con el guardado. No expone la clave."""
        return self.__clave_hash == self._hashear(clave_ingresada)

    def registrar_pedido(self, pedido):
        self._pedidos.append(pedido)

    @property
    def pedidos(self):
        return list(self._pedidos)

    def pedidos_finalizados(self):
        from modelos.pedido import Pedido
        return [p for p in self._pedidos if p.estado == Pedido.FINALIZADO]

    def total_vendido(self):
        return round(sum(p.total() for p in self.pedidos_finalizados()), 2)
