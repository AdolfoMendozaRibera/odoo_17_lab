# -*- coding: utf-8 -*-
import logging
from odoo import models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class OdooDockerInstanceMejoraExt(models.Model):
    """Extiende odoo.docker.instance para evitar iniciar sin plantilla.

    Si el campo ``template_id`` está vacío, el método ``start_instance``
    lanzará un ``UserError`` y no ejecutará los comandos Docker.
    """
    _inherit = 'odoo.docker.instance'

    def start_instance(self):
        """Sobrescribe el arranque de la instancia.

        - Verifica que ``template_id`` esté definido.
        - Si no lo está, muestra un mensaje de error amigable.
        - Si está, delega al comportamiento original mediante ``super``.
        """
        for rec in self:
            if not rec.template_id:
                _logger.warning(
                    "Intento de iniciar instancia %s sin plantilla asignada.", rec.name
                )
                raise UserError(
                    "No se puede iniciar la instancia porque no se ha seleccionado una "
                    "plantilla. Por favor, elija una plantilla antes de iniciar."
                )
        # Llamada al método original (de la clase base) para continuar el proceso.
        return super(OdooDockerInstanceMejoraExt, self).start_instance()
