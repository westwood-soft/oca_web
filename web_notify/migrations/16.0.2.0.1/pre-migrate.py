from odoo.upgrade import util


def migrate(cr, version):
    cr.execute(
        """
            SELECT res_id
              FROM ir_model_data d
             WHERE NOT EXISTS (SELECT 1
                                 FROM ir_model_data
                                WHERE id != d.id
                                  AND res_id = d.res_id
                                  AND model = d.model
                                  AND module != d.module)
               AND module = 'web_notify'
               AND model = 'ir.ui.view'
          ORDER BY id DESC
            """
    )
    for view_id in cr.fetchall():
        util.remove_view(cr, view_id=view_id)

    cr.execute(
        """
            SELECT res_id
              FROM ir_model_data d
             WHERE NOT EXISTS (SELECT 1
                                 FROM ir_model_data
                                WHERE id != d.id
                                  AND res_id = d.res_id
                                  AND model = d.model
                                  AND module != d.module)
               AND module = 'web_notify'
               AND model = 'ir.ui.menu'
          ORDER BY id DESC
    """
    )
    menu_ids = cr.fetchall()
    util.remove_menus(cr, menu_ids)

    cr.execute(
        """
          UPDATE ir_asset SET active = FALSE WHERE name LIKE 'web_notify.%'
        """
    )
