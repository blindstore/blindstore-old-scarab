from blindstore.core.config import cfg

if not cfg.get('ENABLE_CONTRACTS'):
    import contracts
    contracts.disable_all()