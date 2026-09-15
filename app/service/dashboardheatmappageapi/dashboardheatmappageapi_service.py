import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.dashboard_api import (
    fetch_heatmap_cells,
    latest_fiscal_year_id,
    org_from_session,
    paginate_cells,
    set_json_success,
)
from app.dto.dashboardheatmappageapi.dashboardheatmappageapi_dto import DashboardheatmappageapiDto
import utils.string_util


class DashboardheatmappageapiService:

    def dashboardheatmappageapi(self, dashboardheatmappageapi_dto, jsonObj):
        PAGE = utils.string_util.changeNullToBlank(getattr(dashboardheatmappageapi_dto, "page", "") or "1")
        PAGE_SIZE = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmappageapi_dto, "pagesize", "") or "60"
        )
        ROLE_CODE = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmappageapi_dto, "rolecode", "") or "pref"
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            prefecture_code, shokokai_cd = org_from_session(session, dashboardheatmappageapi_dto)
            fiscal_year_id = utils.string_util.changeNullToBlank(
                getattr(dashboardheatmappageapi_dto, "fiscalyearcode", "")
                or getattr(dashboardheatmappageapi_dto, "fiscalyearid", "")
            ) or latest_fiscal_year_id(prefecture_code, shokokai_cd)
            cells = fetch_heatmap_cells(ROLE_CODE, prefecture_code, shokokai_cd, fiscal_year_id)
            page_cells, page, total_pages = paginate_cells(cells, PAGE, PAGE_SIZE)
            set_json_success(
                jsonObj,
                {
                    "cells": page_cells,
                    "page": page,
                    "total_pages": total_pages,
                },
            )
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ヒートマップページ取得に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
            )
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
