import logging

from service.prepare_clothes import prepare_clothes
from service.prepare_colors import prepare_colors
from service.prepare_combinations import prepare_combinations

logger = logging.getLogger(__name__)

logger.info("Prepare tables")
prepare_colors()
prepare_combinations()
prepare_clothes()
