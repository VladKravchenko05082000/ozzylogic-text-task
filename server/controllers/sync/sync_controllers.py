from controllers.sync.rates.controller import (sync_min_fin_bank_rates, sync_nbu_rates)
from controllers.sync.banks.controller import (sync_banks, sync_branches)

def sync_all():
    sync_banks()
    sync_branches()
    sync_min_fin_bank_rates()
    sync_nbu_rates()
