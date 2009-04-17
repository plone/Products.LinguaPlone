import logging


def remove_old_import_step(context):
    # context is portal_setup which is nice
    registry = context.getImportStepRegistry()
    old_step = u'linguaplone_various'
    if old_step in registry.listSteps():
        try:
            registry.unregisterStep(old_step)
        except AttributeError:
            # BBB for GS 1.3
            del registry._registered[old_step]

        # Unfortunately we manually have to signal the context
        # (portal_setup) that it has changed otherwise this change is
        # not persisted.
        context._p_changed = True
        log = logging.getLogger("LinguaPlone")
        log.info("Old %s import step removed from import registry.", old_step)
