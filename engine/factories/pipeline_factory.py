from typing import Callable, Any

from pipelines import bvc_daily


def get_pipeline(pipeline_name: str) -> Callable[..., Any]:

    match pipeline_name:
        case 'bvc_hist':
            return bvc_hist.run
        case 'bvc_daily':
            return bvc_daily.run
        case _:
            return None
