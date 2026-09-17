--
-- PostgreSQL database dump
--

\restrict wNVyToERoDIahowuGxGgQLqqfDZ3xQ0ZuahAV4064jqJNN3a1Zf2VHew2Axdx0a

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS '';


--
-- Name: sp_refresh_kpi_monthly(text); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.sp_refresh_kpi_monthly(IN p_year_month text)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_month_start              DATE := to_date(p_year_month || '-01', 'YYYY-MM-DD');
  v_federation_shokokai_cd    TEXT;
  v_national_prefecture_code  TEXT;
BEGIN
  SELECT setting_value INTO v_federation_shokokai_cd
    FROM mst_system_setting WHERE setting_code = 'federation_shokokai_cd';
  SELECT setting_value INTO v_national_prefecture_code
    FROM mst_system_setting WHERE setting_code = 'national_prefecture_code';

  -- ==========================================================================
  -- trn_kpi_monthly_stat（組織×年度×月ごとの支援件数実績）
  -- ==========================================================================

  -- 1. 各商工会自身の合計行
  INSERT INTO trn_kpi_monthly_stat
    (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd,
     stat_date, support_count, ai_activity_count)
  SELECT prefecture_code, shokokai_cd, fiscal_year_id, NULL, NULL, v_month_start, COUNT(*), 0
  FROM trn_report
  WHERE to_char(report_date, 'YYYY-MM') = p_year_month AND status = '登録済み'
  GROUP BY prefecture_code, shokokai_cd, fiscal_year_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, stat_date)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- 2. 県連ダッシュボードの商工会別内訳行
  INSERT INTO trn_kpi_monthly_stat
    (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd,
     stat_date, support_count, ai_activity_count)
  SELECT prefecture_code, v_federation_shokokai_cd, fiscal_year_id, NULL, shokokai_cd, v_month_start, COUNT(*), 0
  FROM trn_report
  WHERE to_char(report_date, 'YYYY-MM') = p_year_month AND status = '登録済み'
  GROUP BY prefecture_code, shokokai_cd, fiscal_year_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, stat_date)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- 3. 全国ダッシュボードの都道府県別内訳行
  INSERT INTO trn_kpi_monthly_stat
    (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd,
     stat_date, support_count, ai_activity_count)
  SELECT v_national_prefecture_code, v_federation_shokokai_cd, fiscal_year_id, prefecture_code, NULL,
         v_month_start, COUNT(*), 0
  FROM trn_report
  WHERE to_char(report_date, 'YYYY-MM') = p_year_month AND status = '登録済み'
  GROUP BY prefecture_code, fiscal_year_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, stat_date)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- 4a. 各県連自身の合計行
  INSERT INTO trn_kpi_monthly_stat
    (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd,
     stat_date, support_count, ai_activity_count)
  SELECT prefecture_code, v_federation_shokokai_cd, fiscal_year_id, NULL, NULL, v_month_start, COUNT(*), 0
  FROM trn_report
  WHERE to_char(report_date, 'YYYY-MM') = p_year_month AND status = '登録済み'
  GROUP BY prefecture_code, fiscal_year_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, stat_date)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- 4b. 全国連自身の合計行
  INSERT INTO trn_kpi_monthly_stat
    (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd,
     stat_date, support_count, ai_activity_count)
  SELECT v_national_prefecture_code, v_federation_shokokai_cd, fiscal_year_id, NULL, NULL, v_month_start, COUNT(*), 0
  FROM trn_report
  WHERE to_char(report_date, 'YYYY-MM') = p_year_month AND status = '登録済み'
  GROUP BY fiscal_year_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, stat_date)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- ==========================================================================
  -- trn_kpi_theme_breakdown（組織×年度×個別テーマ×年月ごとの支援件数）
  -- ==========================================================================

  -- 1. 各商工会自身の内訳
  INSERT INTO trn_kpi_theme_breakdown (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month, support_count)
  SELECT trn_report.prefecture_code, trn_report.shokokai_cd, trn_report.fiscal_year_id,
         trn_report_theme.theme_id, p_year_month, COUNT(*)
  FROM trn_report
  JOIN trn_report_theme ON trn_report_theme.report_id = trn_report.report_id
  WHERE to_char(trn_report.report_date, 'YYYY-MM') = p_year_month AND trn_report.status = '登録済み'
  GROUP BY trn_report.prefecture_code, trn_report.shokokai_cd, trn_report.fiscal_year_id, trn_report_theme.theme_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- 2. 各県連自身の県内合計
  INSERT INTO trn_kpi_theme_breakdown (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month, support_count)
  SELECT trn_report.prefecture_code, v_federation_shokokai_cd, trn_report.fiscal_year_id,
         trn_report_theme.theme_id, p_year_month, COUNT(*)
  FROM trn_report
  JOIN trn_report_theme ON trn_report_theme.report_id = trn_report.report_id
  WHERE to_char(trn_report.report_date, 'YYYY-MM') = p_year_month AND trn_report.status = '登録済み'
  GROUP BY trn_report.prefecture_code, trn_report.fiscal_year_id, trn_report_theme.theme_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month)
  DO UPDATE SET support_count = EXCLUDED.support_count;

  -- 3. 全国連自身の全国合計
  INSERT INTO trn_kpi_theme_breakdown (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month, support_count)
  SELECT v_national_prefecture_code, v_federation_shokokai_cd, trn_report.fiscal_year_id,
         trn_report_theme.theme_id, p_year_month, COUNT(*)
  FROM trn_report
  JOIN trn_report_theme ON trn_report_theme.report_id = trn_report.report_id
  WHERE to_char(trn_report.report_date, 'YYYY-MM') = p_year_month AND trn_report.status = '登録済み'
  GROUP BY trn_report.fiscal_year_id, trn_report_theme.theme_id
  ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month)
  DO UPDATE SET support_count = EXCLUDED.support_count;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cfg_excel_output_mapping; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cfg_excel_output_mapping (
    mapping_id integer CONSTRAINT mst_excel_output_mapping_mapping_id_not_null NOT NULL,
    form_code text CONSTRAINT mst_excel_output_mapping_form_code_not_null NOT NULL,
    fiscal_year_id integer CONSTRAINT mst_excel_output_mapping_fiscal_year_id_not_null NOT NULL,
    view_column text CONSTRAINT mst_excel_output_mapping_view_column_not_null NOT NULL,
    sheet_name text CONSTRAINT mst_excel_output_mapping_sheet_name_not_null NOT NULL,
    cell_address text CONSTRAINT mst_excel_output_mapping_cell_address_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_excel_output_mapping_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_excel_output_mapping_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    slot_number integer DEFAULT 1 CONSTRAINT mst_excel_output_mapping_slot_number_not_null NOT NULL,
    CONSTRAINT mst_excel_output_mapping_slot_number_check CHECK (((slot_number >= 0) AND (slot_number <= 5)))
);


--
-- Name: cfg_excel_output_mapping_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cfg_excel_output_mapping_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cfg_excel_output_mapping_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cfg_excel_output_mapping_mapping_id_seq OWNED BY public.cfg_excel_output_mapping.mapping_id;


--
-- Name: cfg_excel_report_definition; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cfg_excel_report_definition (
    form_code text CONSTRAINT mst_excel_report_definition_form_code_not_null NOT NULL,
    fiscal_year_id integer CONSTRAINT mst_excel_report_definition_fiscal_year_id_not_null NOT NULL,
    template_filename text CONSTRAINT mst_excel_report_definition_template_filename_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_excel_report_definition_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_excel_report_definition_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    view_name text CONSTRAINT mst_excel_report_definition_view_name_not_null NOT NULL,
    is_day_batch boolean DEFAULT false CONSTRAINT mst_excel_report_definition_is_day_batch_not_null NOT NULL
);


--
-- Name: cfg_menu_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cfg_menu_item (
    role_code text CONSTRAINT mst_menu_item_role_code_not_null1 NOT NULL,
    section_sort_order integer CONSTRAINT mst_menu_item_section_sort_order_not_null1 NOT NULL,
    sort_order integer CONSTRAINT mst_menu_item_sort_order_not_null1 NOT NULL,
    section_label text CONSTRAINT mst_menu_item_section_label_not_null1 NOT NULL,
    label text CONSTRAINT mst_menu_item_label_not_null1 NOT NULL,
    icon text CONSTRAINT mst_menu_item_icon_not_null1 NOT NULL,
    screen_id text CONSTRAINT mst_menu_item_screen_id_not_null1 NOT NULL,
    default_form text,
    requires_capability text,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_menu_item_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_menu_item_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    subtitle text,
    CONSTRAINT mst_menu_item_role_code_check1 CHECK ((role_code = ANY (ARRAY['zenkoku'::text, 'ken'::text, 'shokokai'::text])))
);


--
-- Name: cfg_rag_setting; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cfg_rag_setting (
    rag_setting_id integer CONSTRAINT mst_rag_setting_rag_setting_id_not_null NOT NULL,
    embedding_model text CONSTRAINT mst_rag_setting_embedding_model_not_null NOT NULL,
    vector_db text CONSTRAINT mst_rag_setting_vector_db_not_null NOT NULL,
    chunk_size integer CONSTRAINT mst_rag_setting_chunk_size_not_null NOT NULL,
    chunk_overlap integer CONSTRAINT mst_rag_setting_chunk_overlap_not_null NOT NULL,
    last_synced_at timestamp with time zone CONSTRAINT mst_rag_setting_last_synced_at_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_rag_setting_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_rag_setting_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: cfg_rag_setting_rag_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cfg_rag_setting_rag_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cfg_rag_setting_rag_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cfg_rag_setting_rag_setting_id_seq OWNED BY public.cfg_rag_setting.rag_setting_id;


--
-- Name: cfg_system_setting; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cfg_system_setting (
    setting_code text CONSTRAINT mst_system_setting_setting_code_not_null NOT NULL,
    label text CONSTRAINT mst_system_setting_label_not_null NOT NULL,
    setting_value text CONSTRAINT mst_system_setting_setting_value_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_system_setting_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_system_setting_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_capital_range; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_capital_range (
    capital_range_id integer NOT NULL,
    fiscal_year_id integer NOT NULL,
    capital_range_code text CONSTRAINT mst_capital_range_code_not_null NOT NULL,
    label text NOT NULL,
    sort_order integer NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_capital_range_capital_range_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_capital_range_capital_range_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_capital_range_capital_range_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_capital_range_capital_range_id_seq OWNED BY public.mst_capital_range.capital_range_id;


--
-- Name: mst_employee_range; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_employee_range (
    employee_range_id integer CONSTRAINT mst_employee_count_range_employee_count_range_id_not_null NOT NULL,
    fiscal_year_id integer CONSTRAINT mst_employee_count_range_fiscal_year_id_not_null NOT NULL,
    employee_range_code text CONSTRAINT mst_employee_count_range_code_not_null NOT NULL,
    label text CONSTRAINT mst_employee_count_range_label_not_null NOT NULL,
    sort_order integer CONSTRAINT mst_employee_count_range_sort_order_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_employee_count_range_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_employee_count_range_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_employee_range_employee_range_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_employee_range_employee_range_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_employee_range_employee_range_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_employee_range_employee_range_id_seq OWNED BY public.mst_employee_range.employee_range_id;


--
-- Name: mst_fiscal_year; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_fiscal_year (
    fiscal_year_id integer NOT NULL,
    fiscal_year_code text NOT NULL,
    label text NOT NULL,
    start_month text NOT NULL,
    end_month text NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    stat_as_of_date date
);


--
-- Name: mst_fiscal_year_fiscal_year_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_fiscal_year_fiscal_year_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_fiscal_year_fiscal_year_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_fiscal_year_fiscal_year_id_seq OWNED BY public.mst_fiscal_year.fiscal_year_id;


--
-- Name: mst_form; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_form (
    form_code text CONSTRAINT mst_form_form_code_not_null1 NOT NULL,
    fiscal_year_id integer CONSTRAINT mst_form_fiscal_year_id_not_null1 NOT NULL,
    short_label text CONSTRAINT mst_form_short_label_not_null1 NOT NULL,
    full_label text CONSTRAINT mst_form_full_label_not_null1 NOT NULL,
    badge_class text,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_industry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_industry (
    industry_code text CONSTRAINT mst_industry_industry_code_not_null1 NOT NULL,
    fiscal_year_id integer CONSTRAINT mst_industry_fiscal_year_id_not_null1 NOT NULL,
    label text CONSTRAINT mst_industry_label_not_null1 NOT NULL,
    sort_order integer CONSTRAINT mst_industry_sort_order_not_null1 NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_prefecture; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_prefecture (
    prefecture_code text NOT NULL,
    name text NOT NULL,
    short_name text NOT NULL,
    region text,
    sort_order integer NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT mst_prefecture_prefecture_code_check CHECK ((prefecture_code ~ '^[0-9]{2}$'::text)),
    CONSTRAINT mst_prefecture_region_check CHECK (((region IS NULL) OR (region = ANY (ARRAY['hokkaido'::text, 'tohoku'::text, 'kanto'::text, 'chubu'::text, 'kinki'::text, 'chugoku'::text, 'shikoku'::text, 'kyushu'::text]))))
);


--
-- Name: mst_qualification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_qualification (
    qualification_id integer NOT NULL,
    fiscal_year_id integer NOT NULL,
    qualification_code text NOT NULL,
    label text NOT NULL,
    sort_order integer NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_qualification_qualification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_qualification_qualification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_qualification_qualification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_qualification_qualification_id_seq OWNED BY public.mst_qualification.qualification_id;


--
-- Name: mst_revenue_range; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_revenue_range (
    revenue_range_id integer NOT NULL,
    fiscal_year_id integer NOT NULL,
    revenue_range_code text CONSTRAINT mst_revenue_range_code_not_null NOT NULL,
    label text NOT NULL,
    sort_order integer NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);

--
-- Name: mst_revenue_range_revenue_range_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_revenue_range_revenue_range_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_revenue_range_revenue_range_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_revenue_range_revenue_range_id_seq OWNED BY public.mst_revenue_range.revenue_range_id;


--
-- Name: mst_shokokai; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_shokokai (
    prefecture_code text NOT NULL,
    shokokai_cd text CONSTRAINT mst_shokokai_shokokai_code_not_null NOT NULL,
    name text NOT NULL,
    sort_order integer,
    group_code integer,
    group_label text,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    short_name text NOT NULL,
    CONSTRAINT mst_shokokai_shokokai_code_check CHECK ((shokokai_cd ~ '^[0-9]{4}$'::text))
);


--
-- Name: mst_theme; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_theme (
    theme_id integer CONSTRAINT mst_theme_theme_id_not_null1 NOT NULL,
    fiscal_year_id integer CONSTRAINT mst_theme_fiscal_year_id_not_null1 NOT NULL,
    theme_code text CONSTRAINT mst_theme_theme_code_not_null1 NOT NULL,
    label text CONSTRAINT mst_theme_label_not_null1 NOT NULL,
    badge_class text,
    group_order integer CONSTRAINT mst_theme_group_order_not_null1 NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_theme_created_at_not_null1 NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_theme_updated_at_not_null1 NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_theme_theme_id_seq1; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_theme_theme_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_theme_theme_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_theme_theme_id_seq1 OWNED BY public.mst_theme.theme_id;


--
-- Name: mst_user_account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_user_account (
    user_account_id integer NOT NULL,
    prefecture_code text NOT NULL,
    shokokai_cd text CONSTRAINT mst_user_account_shokokai_code_not_null NOT NULL,
    user_id text CONSTRAINT mst_user_account_staff_code_not_null NOT NULL,
    shokuin_kj text CONSTRAINT mst_user_account_staff_name_not_null NOT NULL,
    email text NOT NULL,
    status integer NOT NULL,
    core_linked boolean DEFAULT false NOT NULL,
    permission_level text NOT NULL,
    last_login_at timestamp with time zone,
    password text,
    totp_secret text,
    is_mfa_enabled boolean DEFAULT false NOT NULL,
    failed_login_count integer DEFAULT 0 NOT NULL,
    locked_until timestamp with time zone,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT mst_user_account_status_check CHECK ((status = ANY (ARRAY[0, 1])))
);


--
-- Name: TABLE mst_user_account; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.mst_user_account IS 'Individual staff members who can log in. Login credentials live here (password, totp_secret) - the only login-credential table in this schema. Role is never stored - it is derived from prefecture_code/shokokai_code (see the note at the top of this file).';


--
-- Name: COLUMN mst_user_account.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.mst_user_account.status IS '1 = active (利用可能), 0 = suspended (利用停止).';


--
-- Name: COLUMN mst_user_account.password; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.mst_user_account.password IS 'TEMPORARY: plaintext, not hashed. App is not internet-facing yet. Must become a hash (werkzeug.security) before public launch - see comment on the table above.';


--
-- Name: COLUMN mst_user_account.totp_secret; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.mst_user_account.totp_secret IS 'Base32 secret for TOTP two-factor authentication (pyotp).';


--
-- Name: mst_user_account_qualification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_user_account_qualification (
    user_account_id integer NOT NULL,
    qualification_id integer NOT NULL
);


--
-- Name: mst_user_account_user_account_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_user_account_user_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_user_account_user_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_user_account_user_account_id_seq OWNED BY public.mst_user_account.user_account_id;


--
-- Name: mst_visit_result; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mst_visit_result (
    visit_result_id integer NOT NULL,
    fiscal_year_id integer NOT NULL,
    visit_result_code text CONSTRAINT mst_visit_result_code_not_null NOT NULL,
    label text NOT NULL,
    sort_order integer NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: mst_visit_result_visit_result_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mst_visit_result_visit_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mst_visit_result_visit_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mst_visit_result_visit_result_id_seq OWNED BY public.mst_visit_result.visit_result_id;


--
-- Name: trn_ai_usage_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_ai_usage_log (
    ai_usage_log_id integer NOT NULL,
    used_at timestamp with time zone DEFAULT now() NOT NULL,
    user_account_id integer,
    feature text NOT NULL,
    input_content text,
    output_content text
);


--
-- Name: trn_ai_usage_log_ai_usage_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_ai_usage_log_ai_usage_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_ai_usage_log_ai_usage_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_ai_usage_log_ai_usage_log_id_seq OWNED BY public.trn_ai_usage_log.ai_usage_log_id;


--
-- Name: trn_change_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_change_history (
    change_history_id integer NOT NULL,
    changed_at timestamp with time zone DEFAULT now() NOT NULL,
    changed_by integer,
    feature text NOT NULL,
    table_name text NOT NULL,
    record_id text NOT NULL,
    action text NOT NULL,
    detail text,
    before_value jsonb,
    after_value jsonb,
    CONSTRAINT trn_change_history_action_check CHECK ((action = ANY (ARRAY['作成'::text, '更新'::text, '削除'::text])))
);


--
-- Name: trn_change_history_change_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_change_history_change_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_change_history_change_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_change_history_change_history_id_seq OWNED BY public.trn_change_history.change_history_id;


--
-- Name: trn_knowledge_document; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_knowledge_document (
    knowledge_document_id integer CONSTRAINT trn_knowledge_document_new_knowledge_document_id_not_null NOT NULL,
    prefecture_code text,
    active_version_number integer CONSTRAINT trn_knowledge_document_new_active_version_number_not_null NOT NULL,
    document_code text CONSTRAINT trn_knowledge_document_new_document_code_not_null NOT NULL,
    title text CONSTRAINT trn_knowledge_document_new_title_not_null NOT NULL,
    category text CONSTRAINT trn_knowledge_document_new_category_not_null NOT NULL,
    format text CONSTRAINT trn_knowledge_document_new_format_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_knowledge_document_new_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_knowledge_document_new_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT trn_knowledge_document_new_format_check CHECK ((format = ANY (ARRAY['PDF'::text, 'Word'::text, 'Excel'::text])))
);


--
-- Name: trn_knowledge_document_knowledge_document_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_knowledge_document_knowledge_document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_knowledge_document_knowledge_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_knowledge_document_knowledge_document_id_seq OWNED BY public.trn_knowledge_document.knowledge_document_id;


--
-- Name: trn_knowledge_document_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_knowledge_document_version (
    knowledge_document_version_id integer CONSTRAINT mst_knowledge_document_vers_knowledge_document_version_not_null NOT NULL,
    knowledge_document_id integer CONSTRAINT mst_knowledge_document_version_knowledge_document_id_not_null NOT NULL,
    version_number integer CONSTRAINT mst_knowledge_document_version_version_number_not_null NOT NULL,
    uploaded_date date CONSTRAINT mst_knowledge_document_version_uploaded_date_not_null NOT NULL,
    uploaded_by text CONSTRAINT mst_knowledge_document_version_uploaded_by_not_null NOT NULL,
    file_size_kb integer CONSTRAINT mst_knowledge_document_version_file_size_kb_not_null NOT NULL,
    status text CONSTRAINT mst_knowledge_document_version_status_not_null NOT NULL,
    file_path text CONSTRAINT mst_knowledge_document_version_file_path_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_knowledge_document_version_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT mst_knowledge_document_version_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT mst_knowledge_document_version_status_check CHECK ((status = ANY (ARRAY['登録済み'::text, '旧版'::text, '処理中'::text, 'エラー'::text])))
);


--
-- Name: trn_knowledge_document_versio_knowledge_document_version_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_knowledge_document_versio_knowledge_document_version_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_knowledge_document_versio_knowledge_document_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_knowledge_document_versio_knowledge_document_version_id_seq OWNED BY public.trn_knowledge_document_version.knowledge_document_version_id;


--
-- Name: trn_knowledge_entry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_knowledge_entry (
    knowledge_entry_id integer CONSTRAINT trn_knowledge_entry_new_knowledge_entry_id_not_null NOT NULL,
    knowledge_document_id integer,
    prefecture_code text,
    knowledge_code text CONSTRAINT trn_knowledge_entry_new_knowledge_code_not_null NOT NULL,
    title text CONSTRAINT trn_knowledge_entry_new_title_not_null NOT NULL,
    updated_date date CONSTRAINT trn_knowledge_entry_new_updated_date_not_null NOT NULL,
    status text CONSTRAINT trn_knowledge_entry_new_status_not_null NOT NULL,
    content text CONSTRAINT trn_knowledge_entry_new_content_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_knowledge_entry_new_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_knowledge_entry_new_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT trn_knowledge_entry_new_status_check CHECK ((status = ANY (ARRAY['公開中'::text, '下書き'::text])))
);


--
-- Name: trn_knowledge_entry_knowledge_entry_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_knowledge_entry_knowledge_entry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_knowledge_entry_knowledge_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_knowledge_entry_knowledge_entry_id_seq OWNED BY public.trn_knowledge_entry.knowledge_entry_id;


--
-- Name: trn_knowledge_entry_theme; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_knowledge_entry_theme (
    knowledge_entry_id integer NOT NULL,
    theme_id integer NOT NULL
);


--
-- Name: trn_kpi_monthly_stat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_kpi_monthly_stat (
    kpi_monthly_stat_id integer CONSTRAINT trn_kpi_daily_kpi_daily_id_not_null NOT NULL,
    prefecture_code text CONSTRAINT trn_kpi_daily_prefecture_code_not_null NOT NULL,
    shokokai_cd text CONSTRAINT trn_kpi_daily_shokokai_cd_not_null NOT NULL,
    fiscal_year_id integer CONSTRAINT trn_kpi_daily_fiscal_year_id_not_null NOT NULL,
    target_prefecture_code text,
    target_shokokai_cd text,
    year_month text CONSTRAINT trn_kpi_daily_stat_date_not_null NOT NULL,
    support_count integer CONSTRAINT trn_kpi_daily_support_count_not_null NOT NULL,
    ai_activity_count integer,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT trn_kpi_daily_check CHECK (((target_prefecture_code IS NULL) OR (target_shokokai_cd IS NULL)))
);


--
-- Name: trn_kpi_monthly_stat_kpi_monthly_stat_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_kpi_monthly_stat_kpi_monthly_stat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_kpi_monthly_stat_kpi_monthly_stat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_kpi_monthly_stat_kpi_monthly_stat_id_seq OWNED BY public.trn_kpi_monthly_stat.kpi_monthly_stat_id;


--
-- Name: trn_kpi_theme_breakdown; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_kpi_theme_breakdown (
    id integer CONSTRAINT trn_kpi_theme_breakdown_new_id_not_null NOT NULL,
    prefecture_code text CONSTRAINT trn_kpi_theme_breakdown_new_prefecture_code_not_null NOT NULL,
    shokokai_cd text CONSTRAINT trn_kpi_theme_breakdown_new_shokokai_cd_not_null NOT NULL,
    fiscal_year_id integer CONSTRAINT trn_kpi_theme_breakdown_new_fiscal_year_id_not_null NOT NULL,
    theme_id integer CONSTRAINT trn_kpi_theme_breakdown_new_theme_id_not_null NOT NULL,
    support_count integer CONSTRAINT trn_kpi_theme_breakdown_new_support_count_not_null NOT NULL,
    year_month text NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: trn_kpi_theme_breakdown_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_kpi_theme_breakdown_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_kpi_theme_breakdown_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_kpi_theme_breakdown_id_seq OWNED BY public.trn_kpi_theme_breakdown.id;


--
-- Name: trn_notice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_notice (
    notice_id integer NOT NULL,
    notice_code text NOT NULL,
    role_code text NOT NULL,
    content text NOT NULL,
    start_date date,
    end_date date,
    sort_order integer DEFAULT 0 NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    CONSTRAINT trn_notice_role_code_check CHECK ((role_code = ANY (ARRAY['login'::text, 'zenkoku'::text, 'ken'::text, 'shokokai'::text])))
);


--
-- Name: trn_notice_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_notice_notice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_notice_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_notice_notice_id_seq OWNED BY public.trn_notice.notice_id;


--
-- Name: trn_report; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_report (
    report_id integer CONSTRAINT trn_report_new_report_id_not_null NOT NULL,
    report_code text CONSTRAINT trn_report_new_report_code_not_null NOT NULL,
    form_code text,
    fiscal_year_id integer CONSTRAINT trn_report_new_fiscal_year_id_not_null NOT NULL,
    prefecture_code text CONSTRAINT trn_report_new_prefecture_code_not_null NOT NULL,
    shokokai_cd text CONSTRAINT trn_report_new_shokokai_cd_not_null NOT NULL,
    theme_id integer,
    industry_code text,
    capital_range_id integer,
    employee_range_id integer,
    revenue_range_id integer,
    expert_qualification_id integer,
    visit_result_id integer,
    report_date date,
    summary text CONSTRAINT trn_report_new_summary_not_null NOT NULL,
    content text,
    voice_transcript text,
    time_start text,
    time_end text,
    business_person text,
    business_name text,
    staff_main_name text,
    staff_sub_name text,
    attendee_count integer,
    expert_name text,
    location text,
    current_issue text,
    support_content text,
    support_result text,
    venue_name text,
    registered_at date,
    status text DEFAULT '登録済み'::text CONSTRAINT trn_report_new_status_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_report_new_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_report_new_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer,
    printed_at date,
    CONSTRAINT trn_report_new_status_check CHECK ((status = ANY (ARRAY['登録済み'::text, '下書き'::text, '削除'::text])))
);


--
-- Name: trn_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_report_report_id_seq OWNED BY public.trn_report.report_id;


--
-- Name: trn_report_theme; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_report_theme (
    report_id integer NOT NULL,
    theme_id integer NOT NULL
);


--
-- Name: trn_trusted_device; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_trusted_device (
    trusted_device_id integer NOT NULL,
    user_account_id integer NOT NULL,
    token_hash text NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) NOT NULL,
    expires_at timestamp with time zone NOT NULL
);


--
-- Name: trn_trusted_device_trusted_device_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_trusted_device_trusted_device_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_trusted_device_trusted_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_trusted_device_trusted_device_id_seq OWNED BY public.trn_trusted_device.trusted_device_id;


--
-- Name: trn_vector_collection; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trn_vector_collection (
    vector_collection_id integer CONSTRAINT trn_vector_collection_new_vector_collection_id_not_null NOT NULL,
    rag_setting_id integer CONSTRAINT trn_vector_collection_new_rag_setting_id_not_null NOT NULL,
    collection_code text CONSTRAINT trn_vector_collection_new_collection_code_not_null NOT NULL,
    name text CONSTRAINT trn_vector_collection_new_name_not_null NOT NULL,
    vector_count integer CONSTRAINT trn_vector_collection_new_vector_count_not_null NOT NULL,
    baseline_vector_count integer CONSTRAINT trn_vector_collection_new_baseline_vector_count_not_null NOT NULL,
    status text CONSTRAINT trn_vector_collection_new_status_not_null NOT NULL,
    synced_date date CONSTRAINT trn_vector_collection_new_synced_date_not_null NOT NULL,
    created_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_vector_collection_new_created_at_not_null NOT NULL,
    created_by integer,
    updated_at text DEFAULT to_char(now(), 'YYYYMMDDHH24MISS'::text) CONSTRAINT trn_vector_collection_new_updated_at_not_null NOT NULL,
    updated_by integer,
    deleted_at text,
    deleted_by integer
);


--
-- Name: trn_vector_collection_vector_collection_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trn_vector_collection_vector_collection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trn_vector_collection_vector_collection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trn_vector_collection_vector_collection_id_seq OWNED BY public.trn_vector_collection.vector_collection_id;


--
-- Name: v_output_f_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_f_excel AS
 SELECT trn_report.report_id,
    mst_form.short_label AS "様式",
    trn_report.report_code AS "報告書番号",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    mst_theme.label AS "支援テーマ",
    mst_industry.label AS "業種",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.staff_main_name AS "担当（主）",
    trn_report.staff_sub_name AS "担当（副）",
    trn_report.summary AS "概要",
    trn_report.content AS "内容"
   FROM (((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_theme ON ((mst_theme.theme_id = trn_report.theme_id)))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
     JOIN public.mst_industry ON (((mst_industry.industry_code = trn_report.industry_code) AND (mst_industry.fiscal_year_id = trn_report.fiscal_year_id))))
  WHERE ((trn_report.form_code = 'F'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g2_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g2_excel AS
 SELECT trn_report.report_id,
    trn_report.report_date,
    trn_report.prefecture_code,
    trn_report.shokokai_cd,
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.summary AS "概要"
   FROM ((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
  WHERE ((trn_report.form_code = 'G-2'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g3_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g3_excel AS
 SELECT trn_report.report_id,
    mst_form.short_label AS "様式",
    trn_report.report_code AS "報告書番号",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    mst_theme.label AS "支援テーマ",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.staff_main_name AS "担当（主）",
    trn_report.staff_sub_name AS "担当（副）",
    trn_report.attendee_count AS "受講者数",
    trn_report.summary AS "概要",
    trn_report.content AS "内容"
   FROM ((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_theme ON ((mst_theme.theme_id = trn_report.theme_id)))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
  WHERE ((trn_report.form_code = 'G-3'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g4_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g4_excel AS
 SELECT trn_report.report_id,
    mst_form.short_label AS "様式",
    trn_report.report_code AS "報告書番号",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    mst_theme.label AS "支援テーマ",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.expert_name AS "専門家氏名",
    mst_capital_range.label AS "資本金",
    mst_employee_range.label AS "従業員数",
    mst_revenue_range.label AS "売上高",
    trn_report.location AS "実施場所",
    mst_qualification.label AS "専門家の資格",
    trn_report.current_issue AS "現状の課題",
    trn_report.support_content AS "支援内容",
    trn_report.support_result AS "支援の成果"
   FROM ((((((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_theme ON ((mst_theme.theme_id = trn_report.theme_id)))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
     LEFT JOIN public.mst_capital_range ON ((mst_capital_range.capital_range_id = trn_report.capital_range_id)))
     LEFT JOIN public.mst_employee_range ON ((mst_employee_range.employee_range_id = trn_report.employee_range_id)))
     LEFT JOIN public.mst_revenue_range ON ((mst_revenue_range.revenue_range_id = trn_report.revenue_range_id)))
     LEFT JOIN public.mst_qualification ON ((mst_qualification.qualification_id = trn_report.expert_qualification_id)))
  WHERE ((trn_report.form_code = 'G-4'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g5_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g5_excel AS
 SELECT trn_report.report_id,
    trn_report.report_date,
    trn_report.prefecture_code,
    trn_report.shokokai_cd,
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.summary AS "概要"
   FROM ((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
  WHERE ((trn_report.form_code = 'G-5'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g6_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g6_excel AS
 SELECT trn_report.report_id,
    mst_form.short_label AS "様式",
    trn_report.report_code AS "報告書番号",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    mst_theme.label AS "支援テーマ",
    trn_report.venue_name AS "会場名",
    trn_report.attendee_count AS "受講者数",
    trn_report.staff_main_name AS "担当（主）",
    trn_report.staff_sub_name AS "担当（副）",
    trn_report.summary AS "概要",
    trn_report.content AS "内容"
   FROM ((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_theme ON ((mst_theme.theme_id = trn_report.theme_id)))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
  WHERE ((trn_report.form_code = 'G-6'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g7_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g7_excel AS
 SELECT trn_report.report_id,
    mst_form.short_label AS "様式",
    trn_report.report_code AS "報告書番号",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    mst_visit_result.label AS "訪問結果",
    trn_report.staff_main_name AS "担当（主）",
    trn_report.staff_sub_name AS "担当（副）",
    trn_report.summary AS "概要",
    trn_report.content AS "内容"
   FROM ((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
     LEFT JOIN public.mst_visit_result ON ((mst_visit_result.visit_result_id = trn_report.visit_result_id)))
  WHERE ((trn_report.form_code = 'G-7'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_g8_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_g8_excel AS
 SELECT trn_report.report_id,
    mst_form.short_label AS "様式",
    trn_report.report_code AS "報告書番号",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    mst_theme.label AS "支援テーマ",
    mst_industry.label AS "業種",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.staff_main_name AS "担当（主）",
    trn_report.staff_sub_name AS "担当（副）",
    trn_report.summary AS "概要",
    trn_report.content AS "内容"
   FROM (((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_theme ON ((mst_theme.theme_id = trn_report.theme_id)))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
     JOIN public.mst_industry ON (((mst_industry.industry_code = trn_report.industry_code) AND (mst_industry.fiscal_year_id = trn_report.fiscal_year_id))))
  WHERE ((trn_report.form_code = 'G-8'::text) AND (trn_report.status = '登録済み'::text));


--
-- Name: v_output_h_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_h_excel AS
 SELECT totals.prefecture_code,
    totals.shokokai_cd,
    totals.fiscal_year_id,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    totals.support_count AS "年間支援件数",
    totals.ai_activity_count AS "年間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((( SELECT trn_kpi_monthly_stat.prefecture_code,
            trn_kpi_monthly_stat.shokokai_cd,
            trn_kpi_monthly_stat.fiscal_year_id,
            sum(trn_kpi_monthly_stat.support_count) AS support_count,
            sum(trn_kpi_monthly_stat.ai_activity_count) AS ai_activity_count
           FROM public.trn_kpi_monthly_stat
          WHERE ((trn_kpi_monthly_stat.target_prefecture_code IS NULL) AND (trn_kpi_monthly_stat.target_shokokai_cd IS NULL))
          GROUP BY trn_kpi_monthly_stat.prefecture_code, trn_kpi_monthly_stat.shokokai_cd, trn_kpi_monthly_stat.fiscal_year_id) totals
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = totals.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = totals.prefecture_code) AND (mst_shokokai.shokokai_cd = totals.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = totals.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'H'::text) AND (mst_form.fiscal_year_id = totals.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            sum(b.support_count) AS support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = totals.prefecture_code) AND (b.shokokai_cd = totals.shokokai_cd) AND (b.fiscal_year_id = totals.fiscal_year_id))
          GROUP BY mst_theme.theme_id, mst_theme.label
          ORDER BY (sum(b.support_count)) DESC
         LIMIT 1) top_theme ON (true));


--
-- Name: v_output_i1_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i1_excel AS
 SELECT totals.prefecture_code,
    totals.shokokai_cd,
    totals.fiscal_year_id,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    totals.support_count AS "年間支援件数",
    totals.ai_activity_count AS "年間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((( SELECT trn_kpi_monthly_stat.prefecture_code,
            trn_kpi_monthly_stat.shokokai_cd,
            trn_kpi_monthly_stat.fiscal_year_id,
            sum(trn_kpi_monthly_stat.support_count) AS support_count,
            sum(trn_kpi_monthly_stat.ai_activity_count) AS ai_activity_count
           FROM public.trn_kpi_monthly_stat
          WHERE ((trn_kpi_monthly_stat.target_prefecture_code IS NULL) AND (trn_kpi_monthly_stat.target_shokokai_cd IS NULL))
          GROUP BY trn_kpi_monthly_stat.prefecture_code, trn_kpi_monthly_stat.shokokai_cd, trn_kpi_monthly_stat.fiscal_year_id) totals
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = totals.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = totals.prefecture_code) AND (mst_shokokai.shokokai_cd = totals.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = totals.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-1'::text) AND (mst_form.fiscal_year_id = totals.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            sum(b.support_count) AS support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = totals.prefecture_code) AND (b.shokokai_cd = totals.shokokai_cd) AND (b.fiscal_year_id = totals.fiscal_year_id))
          GROUP BY mst_theme.theme_id, mst_theme.label
          ORDER BY (sum(b.support_count)) DESC
         LIMIT 1) top_theme ON (true));


--
-- Name: v_output_i2_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i2_excel AS
 SELECT stat.prefecture_code,
    stat.shokokai_cd,
    stat.fiscal_year_id,
    stat.year_month,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    stat.year_month AS "対象年月",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    stat.support_count AS "月間支援件数",
    stat.ai_activity_count AS "月間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((public.trn_kpi_monthly_stat stat
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = stat.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = stat.prefecture_code) AND (mst_shokokai.shokokai_cd = stat.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = stat.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-2'::text) AND (mst_form.fiscal_year_id = stat.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            b.support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = stat.prefecture_code) AND (b.shokokai_cd = stat.shokokai_cd) AND (b.fiscal_year_id = stat.fiscal_year_id) AND (b.year_month = stat.year_month))
          ORDER BY b.support_count DESC
         LIMIT 1) top_theme ON (true))
  WHERE ((stat.target_prefecture_code IS NULL) AND (stat.target_shokokai_cd IS NULL));


--
-- Name: v_output_i3_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i3_excel AS
 SELECT stat.prefecture_code,
    stat.shokokai_cd,
    stat.fiscal_year_id,
    stat.year_month,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    stat.year_month AS "対象年月",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    stat.support_count AS "月間支援件数",
    stat.ai_activity_count AS "月間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((public.trn_kpi_monthly_stat stat
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = stat.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = stat.prefecture_code) AND (mst_shokokai.shokokai_cd = stat.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = stat.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-3'::text) AND (mst_form.fiscal_year_id = stat.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            b.support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = stat.prefecture_code) AND (b.shokokai_cd = stat.shokokai_cd) AND (b.fiscal_year_id = stat.fiscal_year_id) AND (b.year_month = stat.year_month))
          ORDER BY b.support_count DESC
         LIMIT 1) top_theme ON (true))
  WHERE ((stat.target_prefecture_code IS NULL) AND (stat.target_shokokai_cd IS NULL));


--
-- Name: v_output_i4_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i4_excel AS
 SELECT stat.prefecture_code,
    stat.shokokai_cd,
    stat.fiscal_year_id,
    stat.year_month,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    stat.year_month AS "対象年月",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    stat.support_count AS "月間支援件数",
    stat.ai_activity_count AS "月間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((public.trn_kpi_monthly_stat stat
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = stat.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = stat.prefecture_code) AND (mst_shokokai.shokokai_cd = stat.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = stat.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-4'::text) AND (mst_form.fiscal_year_id = stat.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            b.support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = stat.prefecture_code) AND (b.shokokai_cd = stat.shokokai_cd) AND (b.fiscal_year_id = stat.fiscal_year_id) AND (b.year_month = stat.year_month))
          ORDER BY b.support_count DESC
         LIMIT 1) top_theme ON (true))
  WHERE ((stat.target_prefecture_code IS NULL) AND (stat.target_shokokai_cd IS NULL));


--
-- Name: v_output_i5_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i5_excel AS
 SELECT stat.prefecture_code,
    stat.shokokai_cd,
    stat.fiscal_year_id,
    stat.year_month,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    stat.year_month AS "対象年月",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    stat.support_count AS "月間支援件数",
    stat.ai_activity_count AS "月間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((public.trn_kpi_monthly_stat stat
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = stat.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = stat.prefecture_code) AND (mst_shokokai.shokokai_cd = stat.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = stat.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-5'::text) AND (mst_form.fiscal_year_id = stat.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            b.support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = stat.prefecture_code) AND (b.shokokai_cd = stat.shokokai_cd) AND (b.fiscal_year_id = stat.fiscal_year_id) AND (b.year_month = stat.year_month))
          ORDER BY b.support_count DESC
         LIMIT 1) top_theme ON (true))
  WHERE ((stat.target_prefecture_code IS NULL) AND (stat.target_shokokai_cd IS NULL));


--
-- Name: v_output_i6_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i6_excel AS
 SELECT totals.prefecture_code,
    totals.shokokai_cd,
    totals.fiscal_year_id,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    totals.support_count AS "年間支援件数",
    totals.ai_activity_count AS "年間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((( SELECT trn_kpi_monthly_stat.prefecture_code,
            trn_kpi_monthly_stat.shokokai_cd,
            trn_kpi_monthly_stat.fiscal_year_id,
            sum(trn_kpi_monthly_stat.support_count) AS support_count,
            sum(trn_kpi_monthly_stat.ai_activity_count) AS ai_activity_count
           FROM public.trn_kpi_monthly_stat
          WHERE ((trn_kpi_monthly_stat.target_prefecture_code IS NULL) AND (trn_kpi_monthly_stat.target_shokokai_cd IS NULL))
          GROUP BY trn_kpi_monthly_stat.prefecture_code, trn_kpi_monthly_stat.shokokai_cd, trn_kpi_monthly_stat.fiscal_year_id) totals
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = totals.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = totals.prefecture_code) AND (mst_shokokai.shokokai_cd = totals.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = totals.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-6'::text) AND (mst_form.fiscal_year_id = totals.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            sum(b.support_count) AS support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = totals.prefecture_code) AND (b.shokokai_cd = totals.shokokai_cd) AND (b.fiscal_year_id = totals.fiscal_year_id))
          GROUP BY mst_theme.theme_id, mst_theme.label
          ORDER BY (sum(b.support_count)) DESC
         LIMIT 1) top_theme ON (true));


--
-- Name: v_output_i7_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i7_excel AS
 SELECT totals.prefecture_code,
    totals.shokokai_cd,
    totals.fiscal_year_id,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    totals.support_count AS "年間支援件数",
    totals.ai_activity_count AS "年間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((( SELECT trn_kpi_monthly_stat.prefecture_code,
            trn_kpi_monthly_stat.shokokai_cd,
            trn_kpi_monthly_stat.fiscal_year_id,
            sum(trn_kpi_monthly_stat.support_count) AS support_count,
            sum(trn_kpi_monthly_stat.ai_activity_count) AS ai_activity_count
           FROM public.trn_kpi_monthly_stat
          WHERE ((trn_kpi_monthly_stat.target_prefecture_code IS NULL) AND (trn_kpi_monthly_stat.target_shokokai_cd IS NULL))
          GROUP BY trn_kpi_monthly_stat.prefecture_code, trn_kpi_monthly_stat.shokokai_cd, trn_kpi_monthly_stat.fiscal_year_id) totals
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = totals.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = totals.prefecture_code) AND (mst_shokokai.shokokai_cd = totals.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = totals.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-7'::text) AND (mst_form.fiscal_year_id = totals.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            sum(b.support_count) AS support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = totals.prefecture_code) AND (b.shokokai_cd = totals.shokokai_cd) AND (b.fiscal_year_id = totals.fiscal_year_id))
          GROUP BY mst_theme.theme_id, mst_theme.label
          ORDER BY (sum(b.support_count)) DESC
         LIMIT 1) top_theme ON (true));


--
-- Name: v_output_i8_excel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_i8_excel AS
 SELECT totals.prefecture_code,
    totals.shokokai_cd,
    totals.fiscal_year_id,
    mst_form.short_label AS "様式",
    mst_fiscal_year.label AS "対象年度",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    totals.support_count AS "年間支援件数",
    totals.ai_activity_count AS "年間AI活用件数",
    top_theme.label AS "最多支援テーマ",
    top_theme.support_count AS "最多支援テーマ件数"
   FROM (((((( SELECT trn_kpi_monthly_stat.prefecture_code,
            trn_kpi_monthly_stat.shokokai_cd,
            trn_kpi_monthly_stat.fiscal_year_id,
            sum(trn_kpi_monthly_stat.support_count) AS support_count,
            sum(trn_kpi_monthly_stat.ai_activity_count) AS ai_activity_count
           FROM public.trn_kpi_monthly_stat
          WHERE ((trn_kpi_monthly_stat.target_prefecture_code IS NULL) AND (trn_kpi_monthly_stat.target_shokokai_cd IS NULL))
          GROUP BY trn_kpi_monthly_stat.prefecture_code, trn_kpi_monthly_stat.shokokai_cd, trn_kpi_monthly_stat.fiscal_year_id) totals
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = totals.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = totals.prefecture_code) AND (mst_shokokai.shokokai_cd = totals.shokokai_cd))))
     JOIN public.mst_fiscal_year ON ((mst_fiscal_year.fiscal_year_id = totals.fiscal_year_id)))
     JOIN public.mst_form ON (((mst_form.form_code = 'I-8'::text) AND (mst_form.fiscal_year_id = totals.fiscal_year_id))))
     LEFT JOIN LATERAL ( SELECT mst_theme.label,
            sum(b.support_count) AS support_count
           FROM (public.trn_kpi_theme_breakdown b
             JOIN public.mst_theme ON ((mst_theme.theme_id = b.theme_id)))
          WHERE ((b.prefecture_code = totals.prefecture_code) AND (b.shokokai_cd = totals.shokokai_cd) AND (b.fiscal_year_id = totals.fiscal_year_id))
          GROUP BY mst_theme.theme_id, mst_theme.label
          ORDER BY (sum(b.support_count)) DESC
         LIMIT 1) top_theme ON (true));


--
-- Name: v_output_reports_csv; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_output_reports_csv AS
 SELECT trn_report.report_id,
    trn_report.prefecture_code,
    trn_report.shokokai_cd,
    mst_form.short_label AS "様式",
    mst_prefecture.name AS "都道府県連",
    mst_shokokai.name AS "商工会",
    trn_report.report_code AS "報告書番号",
    mst_theme.label AS "支援テーマ",
    mst_industry.label AS "業種",
    trn_report.report_date AS "実施日",
    trn_report.time_start AS "開始時刻",
    trn_report.time_end AS "終了時刻",
    trn_report.business_name AS "事業所名",
    trn_report.business_person AS "担当者名",
    trn_report.summary AS "概要",
    trn_report.content AS "内容",
    trn_report.voice_transcript AS "音声入力の変換結果",
    trn_report.staff_main_name AS "担当（主）",
    trn_report.staff_sub_name AS "担当（副）",
    trn_report.registered_at AS "登録日"
   FROM (((((public.trn_report
     JOIN public.mst_prefecture ON ((mst_prefecture.prefecture_code = trn_report.prefecture_code)))
     JOIN public.mst_shokokai ON (((mst_shokokai.prefecture_code = trn_report.prefecture_code) AND (mst_shokokai.shokokai_cd = trn_report.shokokai_cd))))
     JOIN public.mst_theme ON ((mst_theme.theme_id = trn_report.theme_id)))
     JOIN public.mst_form ON (((mst_form.form_code = trn_report.form_code) AND (mst_form.fiscal_year_id = trn_report.fiscal_year_id))))
     JOIN public.mst_industry ON (((mst_industry.industry_code = trn_report.industry_code) AND (mst_industry.fiscal_year_id = trn_report.fiscal_year_id))))
  WHERE (trn_report.status = '登録済み'::text);


--
-- Name: cfg_excel_output_mapping mapping_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_excel_output_mapping ALTER COLUMN mapping_id SET DEFAULT nextval('public.cfg_excel_output_mapping_mapping_id_seq'::regclass);


--
-- Name: cfg_rag_setting rag_setting_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_rag_setting ALTER COLUMN rag_setting_id SET DEFAULT nextval('public.cfg_rag_setting_rag_setting_id_seq'::regclass);


--
-- Name: mst_capital_range capital_range_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_capital_range ALTER COLUMN capital_range_id SET DEFAULT nextval('public.mst_capital_range_capital_range_id_seq'::regclass);


--
-- Name: mst_employee_range employee_range_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_employee_range ALTER COLUMN employee_range_id SET DEFAULT nextval('public.mst_employee_range_employee_range_id_seq'::regclass);


--
-- Name: mst_fiscal_year fiscal_year_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_fiscal_year ALTER COLUMN fiscal_year_id SET DEFAULT nextval('public.mst_fiscal_year_fiscal_year_id_seq'::regclass);


--
-- Name: mst_qualification qualification_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_qualification ALTER COLUMN qualification_id SET DEFAULT nextval('public.mst_qualification_qualification_id_seq'::regclass);


--
-- Name: mst_revenue_range revenue_range_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_revenue_range ALTER COLUMN revenue_range_id SET DEFAULT nextval('public.mst_revenue_range_revenue_range_id_seq'::regclass);


--
-- Name: mst_theme theme_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme ALTER COLUMN theme_id SET DEFAULT nextval('public.mst_theme_theme_id_seq1'::regclass);


--
-- Name: mst_user_account user_account_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account ALTER COLUMN user_account_id SET DEFAULT nextval('public.mst_user_account_user_account_id_seq'::regclass);


--
-- Name: mst_visit_result visit_result_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_visit_result ALTER COLUMN visit_result_id SET DEFAULT nextval('public.mst_visit_result_visit_result_id_seq'::regclass);


--
-- Name: trn_ai_usage_log ai_usage_log_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_ai_usage_log ALTER COLUMN ai_usage_log_id SET DEFAULT nextval('public.trn_ai_usage_log_ai_usage_log_id_seq'::regclass);


--
-- Name: trn_change_history change_history_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_change_history ALTER COLUMN change_history_id SET DEFAULT nextval('public.trn_change_history_change_history_id_seq'::regclass);


--
-- Name: trn_knowledge_document knowledge_document_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document ALTER COLUMN knowledge_document_id SET DEFAULT nextval('public.trn_knowledge_document_knowledge_document_id_seq'::regclass);


--
-- Name: trn_knowledge_document_version knowledge_document_version_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version ALTER COLUMN knowledge_document_version_id SET DEFAULT nextval('public.trn_knowledge_document_versio_knowledge_document_version_id_seq'::regclass);


--
-- Name: trn_knowledge_entry knowledge_entry_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry ALTER COLUMN knowledge_entry_id SET DEFAULT nextval('public.trn_knowledge_entry_knowledge_entry_id_seq'::regclass);


--
-- Name: trn_kpi_monthly_stat kpi_monthly_stat_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat ALTER COLUMN kpi_monthly_stat_id SET DEFAULT nextval('public.trn_kpi_monthly_stat_kpi_monthly_stat_id_seq'::regclass);


--
-- Name: trn_kpi_theme_breakdown id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown ALTER COLUMN id SET DEFAULT nextval('public.trn_kpi_theme_breakdown_id_seq'::regclass);


--
-- Name: trn_notice notice_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_notice ALTER COLUMN notice_id SET DEFAULT nextval('public.trn_notice_notice_id_seq'::regclass);


--
-- Name: trn_report report_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report ALTER COLUMN report_id SET DEFAULT nextval('public.trn_report_report_id_seq'::regclass);


--
-- Name: trn_trusted_device trusted_device_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_trusted_device ALTER COLUMN trusted_device_id SET DEFAULT nextval('public.trn_trusted_device_trusted_device_id_seq'::regclass);


--
-- Name: trn_vector_collection vector_collection_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection ALTER COLUMN vector_collection_id SET DEFAULT nextval('public.trn_vector_collection_vector_collection_id_seq'::regclass);


--
-- Data for Name: cfg_excel_output_mapping; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cfg_excel_output_mapping (mapping_id, form_code, fiscal_year_id, view_column, sheet_name, cell_address, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by, slot_number) FROM stdin;
16	G-2	3	実施日	Sheet1	B2	20260813065853	\N	20260813065853	\N	\N	\N	0
17	G-2	3	都道府県連	Sheet1	B3	20260813065853	\N	20260813065853	\N	\N	\N	0
18	G-2	3	商工会	Sheet1	D3	20260813065853	\N	20260813065853	\N	\N	\N	0
19	G-2	3	開始時刻	Sheet1	B7	20260813065853	\N	20260813065853	\N	\N	\N	1
20	G-2	3	終了時刻	Sheet1	C7	20260813065853	\N	20260813065853	\N	\N	\N	1
21	G-2	3	事業所名	Sheet1	D7	20260813065853	\N	20260813065853	\N	\N	\N	1
22	G-2	3	担当者名	Sheet1	E7	20260813065853	\N	20260813065853	\N	\N	\N	1
23	G-2	3	概要	Sheet1	F7	20260813065853	\N	20260813065853	\N	\N	\N	1
24	G-2	3	開始時刻	Sheet1	B8	20260813065853	\N	20260813065853	\N	\N	\N	2
25	G-2	3	終了時刻	Sheet1	C8	20260813065853	\N	20260813065853	\N	\N	\N	2
26	G-2	3	事業所名	Sheet1	D8	20260813065853	\N	20260813065853	\N	\N	\N	2
27	G-2	3	担当者名	Sheet1	E8	20260813065853	\N	20260813065853	\N	\N	\N	2
28	G-2	3	概要	Sheet1	F8	20260813065853	\N	20260813065853	\N	\N	\N	2
29	G-2	3	開始時刻	Sheet1	B9	20260813065853	\N	20260813065853	\N	\N	\N	3
30	G-2	3	終了時刻	Sheet1	C9	20260813065853	\N	20260813065853	\N	\N	\N	3
31	G-2	3	事業所名	Sheet1	D9	20260813065853	\N	20260813065853	\N	\N	\N	3
32	G-2	3	担当者名	Sheet1	E9	20260813065853	\N	20260813065853	\N	\N	\N	3
33	G-2	3	概要	Sheet1	F9	20260813065853	\N	20260813065853	\N	\N	\N	3
34	G-2	3	開始時刻	Sheet1	B10	20260813065853	\N	20260813065853	\N	\N	\N	4
35	G-2	3	終了時刻	Sheet1	C10	20260813065853	\N	20260813065853	\N	\N	\N	4
36	G-2	3	事業所名	Sheet1	D10	20260813065853	\N	20260813065853	\N	\N	\N	4
37	G-2	3	担当者名	Sheet1	E10	20260813065853	\N	20260813065853	\N	\N	\N	4
38	G-2	3	概要	Sheet1	F10	20260813065853	\N	20260813065853	\N	\N	\N	4
39	G-2	3	開始時刻	Sheet1	B11	20260813065853	\N	20260813065853	\N	\N	\N	5
40	G-2	3	終了時刻	Sheet1	C11	20260813065853	\N	20260813065853	\N	\N	\N	5
41	G-2	3	事業所名	Sheet1	D11	20260813065853	\N	20260813065853	\N	\N	\N	5
42	G-2	3	担当者名	Sheet1	E11	20260813065853	\N	20260813065853	\N	\N	\N	5
43	G-2	3	概要	Sheet1	F11	20260813065853	\N	20260813065853	\N	\N	\N	5
44	G-5	3	実施日	Sheet1	B2	20260813065853	\N	20260813065853	\N	\N	\N	0
45	G-5	3	都道府県連	Sheet1	B3	20260813065853	\N	20260813065853	\N	\N	\N	0
46	G-5	3	商工会	Sheet1	D3	20260813065853	\N	20260813065853	\N	\N	\N	0
47	G-5	3	開始時刻	Sheet1	B7	20260813065853	\N	20260813065853	\N	\N	\N	1
48	G-5	3	終了時刻	Sheet1	C7	20260813065853	\N	20260813065853	\N	\N	\N	1
49	G-5	3	事業所名	Sheet1	D7	20260813065853	\N	20260813065853	\N	\N	\N	1
50	G-5	3	担当者名	Sheet1	E7	20260813065853	\N	20260813065853	\N	\N	\N	1
51	G-5	3	概要	Sheet1	F7	20260813065853	\N	20260813065853	\N	\N	\N	1
52	G-5	3	開始時刻	Sheet1	B8	20260813065853	\N	20260813065853	\N	\N	\N	2
53	G-5	3	終了時刻	Sheet1	C8	20260813065853	\N	20260813065853	\N	\N	\N	2
54	G-5	3	事業所名	Sheet1	D8	20260813065853	\N	20260813065853	\N	\N	\N	2
55	G-5	3	担当者名	Sheet1	E8	20260813065853	\N	20260813065853	\N	\N	\N	2
56	G-5	3	概要	Sheet1	F8	20260813065853	\N	20260813065853	\N	\N	\N	2
57	G-5	3	開始時刻	Sheet1	B9	20260813065853	\N	20260813065853	\N	\N	\N	3
58	G-5	3	終了時刻	Sheet1	C9	20260813065853	\N	20260813065853	\N	\N	\N	3
59	G-5	3	事業所名	Sheet1	D9	20260813065853	\N	20260813065853	\N	\N	\N	3
60	G-5	3	担当者名	Sheet1	E9	20260813065853	\N	20260813065853	\N	\N	\N	3
61	G-5	3	概要	Sheet1	F9	20260813065853	\N	20260813065853	\N	\N	\N	3
62	G-5	3	開始時刻	Sheet1	B10	20260813065853	\N	20260813065853	\N	\N	\N	4
63	G-5	3	終了時刻	Sheet1	C10	20260813065853	\N	20260813065853	\N	\N	\N	4
64	G-5	3	事業所名	Sheet1	D10	20260813065853	\N	20260813065853	\N	\N	\N	4
65	G-5	3	担当者名	Sheet1	E10	20260813065853	\N	20260813065853	\N	\N	\N	4
66	G-5	3	概要	Sheet1	F10	20260813065853	\N	20260813065853	\N	\N	\N	4
67	G-5	3	開始時刻	Sheet1	B11	20260813065853	\N	20260813065853	\N	\N	\N	5
68	G-5	3	終了時刻	Sheet1	C11	20260813065853	\N	20260813065853	\N	\N	\N	5
69	G-5	3	事業所名	Sheet1	D11	20260813065853	\N	20260813065853	\N	\N	\N	5
70	G-5	3	担当者名	Sheet1	E11	20260813065853	\N	20260813065853	\N	\N	\N	5
71	G-5	3	概要	Sheet1	F11	20260813065853	\N	20260813065853	\N	\N	\N	5
72	G-3	3	様式	Sheet1	B2	20260813065853	\N	20260813065853	\N	\N	\N	1
73	G-3	3	報告書番号	Sheet1	F2	20260813065853	\N	20260813065853	\N	\N	\N	1
74	G-3	3	都道府県連	Sheet1	B3	20260813065853	\N	20260813065853	\N	\N	\N	1
75	G-3	3	商工会	Sheet1	B4	20260813065853	\N	20260813065853	\N	\N	\N	1
76	G-3	3	実施日	Sheet1	B5	20260813065853	\N	20260813065853	\N	\N	\N	1
77	G-3	3	開始時刻	Sheet1	D5	20260813065853	\N	20260813065853	\N	\N	\N	1
78	G-3	3	終了時刻	Sheet1	F5	20260813065853	\N	20260813065853	\N	\N	\N	1
79	G-3	3	支援テーマ	Sheet1	B6	20260813065853	\N	20260813065853	\N	\N	\N	1
80	G-3	3	事業所名	Sheet1	B7	20260813065853	\N	20260813065853	\N	\N	\N	1
81	G-3	3	担当者名	Sheet1	D7	20260813065853	\N	20260813065853	\N	\N	\N	1
82	G-3	3	担当（主）	Sheet1	B8	20260813065853	\N	20260813065853	\N	\N	\N	1
83	G-3	3	担当（副）	Sheet1	D8	20260813065853	\N	20260813065853	\N	\N	\N	1
84	G-3	3	受講者数	Sheet1	F8	20260813065853	\N	20260813065853	\N	\N	\N	1
85	G-3	3	概要	Sheet1	B9	20260813065853	\N	20260813065853	\N	\N	\N	1
86	G-3	3	内容	Sheet1	B10	20260813065853	\N	20260813065853	\N	\N	\N	1
87	G-4	3	様式	Sheet1	B2	20260813065853	\N	20260813065853	\N	\N	\N	1
88	G-4	3	報告書番号	Sheet1	F2	20260813065853	\N	20260813065853	\N	\N	\N	1
89	G-4	3	都道府県連	Sheet1	B3	20260813065853	\N	20260813065853	\N	\N	\N	1
90	G-4	3	商工会	Sheet1	B4	20260813065853	\N	20260813065853	\N	\N	\N	1
91	G-4	3	実施日	Sheet1	B5	20260813065853	\N	20260813065853	\N	\N	\N	1
92	G-4	3	開始時刻	Sheet1	D5	20260813065853	\N	20260813065853	\N	\N	\N	1
93	G-4	3	終了時刻	Sheet1	F5	20260813065853	\N	20260813065853	\N	\N	\N	1
94	G-4	3	支援テーマ	Sheet1	B6	20260813065853	\N	20260813065853	\N	\N	\N	1
95	G-4	3	事業所名	Sheet1	B7	20260813065853	\N	20260813065853	\N	\N	\N	1
96	G-4	3	担当者名	Sheet1	D7	20260813065853	\N	20260813065853	\N	\N	\N	1
97	G-4	3	専門家氏名	Sheet1	B8	20260813065853	\N	20260813065853	\N	\N	\N	1
98	G-4	3	専門家の資格	Sheet1	D8	20260813065853	\N	20260813065853	\N	\N	\N	1
99	G-4	3	資本金	Sheet1	B9	20260813065853	\N	20260813065853	\N	\N	\N	1
100	G-4	3	従業員数	Sheet1	D9	20260813065853	\N	20260813065853	\N	\N	\N	1
101	G-4	3	売上高	Sheet1	F9	20260813065853	\N	20260813065853	\N	\N	\N	1
102	G-4	3	実施場所	Sheet1	B10	20260813065853	\N	20260813065853	\N	\N	\N	1
103	G-4	3	現状の課題	Sheet1	B11	20260813065853	\N	20260813065853	\N	\N	\N	1
104	G-4	3	支援内容	Sheet1	B12	20260813065853	\N	20260813065853	\N	\N	\N	1
105	G-4	3	支援の成果	Sheet1	B13	20260813065853	\N	20260813065853	\N	\N	\N	1
106	G-6	3	様式	Sheet1	B2	20260813065853	\N	20260813065853	\N	\N	\N	1
107	G-6	3	報告書番号	Sheet1	F2	20260813065853	\N	20260813065853	\N	\N	\N	1
108	G-6	3	都道府県連	Sheet1	B3	20260813065853	\N	20260813065853	\N	\N	\N	1
109	G-6	3	商工会	Sheet1	B4	20260813065853	\N	20260813065853	\N	\N	\N	1
110	G-6	3	実施日	Sheet1	B5	20260813065853	\N	20260813065853	\N	\N	\N	1
111	G-6	3	開始時刻	Sheet1	D5	20260813065853	\N	20260813065853	\N	\N	\N	1
112	G-6	3	終了時刻	Sheet1	F5	20260813065853	\N	20260813065853	\N	\N	\N	1
113	G-6	3	支援テーマ	Sheet1	B6	20260813065853	\N	20260813065853	\N	\N	\N	1
114	G-6	3	会場名	Sheet1	B7	20260813065853	\N	20260813065853	\N	\N	\N	1
115	G-6	3	受講者数	Sheet1	D7	20260813065853	\N	20260813065853	\N	\N	\N	1
116	G-6	3	担当（主）	Sheet1	B8	20260813065853	\N	20260813065853	\N	\N	\N	1
117	G-6	3	担当（副）	Sheet1	D8	20260813065853	\N	20260813065853	\N	\N	\N	1
118	G-6	3	概要	Sheet1	B9	20260813065853	\N	20260813065853	\N	\N	\N	1
119	G-6	3	内容	Sheet1	B10	20260813065853	\N	20260813065853	\N	\N	\N	1
120	G-7	3	様式	Sheet1	B2	20260813065853	\N	20260813065853	\N	\N	\N	1
121	G-7	3	報告書番号	Sheet1	F2	20260813065853	\N	20260813065853	\N	\N	\N	1
122	G-7	3	都道府県連	Sheet1	B3	20260813065853	\N	20260813065853	\N	\N	\N	1
123	G-7	3	商工会	Sheet1	B4	20260813065853	\N	20260813065853	\N	\N	\N	1
124	G-7	3	実施日	Sheet1	B5	20260813065853	\N	20260813065853	\N	\N	\N	1
125	G-7	3	開始時刻	Sheet1	D5	20260813065853	\N	20260813065853	\N	\N	\N	1
126	G-7	3	終了時刻	Sheet1	F5	20260813065853	\N	20260813065853	\N	\N	\N	1
127	G-7	3	事業所名	Sheet1	B6	20260813065853	\N	20260813065853	\N	\N	\N	1
128	G-7	3	担当者名	Sheet1	D6	20260813065853	\N	20260813065853	\N	\N	\N	1
129	G-7	3	訪問結果	Sheet1	B7	20260813065853	\N	20260813065853	\N	\N	\N	1
130	G-7	3	担当（主）	Sheet1	B8	20260813065853	\N	20260813065853	\N	\N	\N	1
131	G-7	3	担当（副）	Sheet1	D8	20260813065853	\N	20260813065853	\N	\N	\N	1
132	G-7	3	概要	Sheet1	B9	20260813065853	\N	20260813065853	\N	\N	\N	1
133	G-7	3	内容	Sheet1	B10	20260813065853	\N	20260813065853	\N	\N	\N	1
134	F	3	様式	Sheet1	B2	20260813092223	\N	20260813092223	\N	\N	\N	1
135	F	3	報告書番号	Sheet1	F2	20260813092223	\N	20260813092223	\N	\N	\N	1
136	F	3	都道府県連	Sheet1	B3	20260813092223	\N	20260813092223	\N	\N	\N	1
137	F	3	商工会	Sheet1	B4	20260813092223	\N	20260813092223	\N	\N	\N	1
138	F	3	実施日	Sheet1	B5	20260813092223	\N	20260813092223	\N	\N	\N	1
139	F	3	開始時刻	Sheet1	D5	20260813092223	\N	20260813092223	\N	\N	\N	1
140	F	3	終了時刻	Sheet1	F5	20260813092223	\N	20260813092223	\N	\N	\N	1
141	F	3	支援テーマ	Sheet1	B6	20260813092223	\N	20260813092223	\N	\N	\N	1
142	F	3	業種	Sheet1	D6	20260813092223	\N	20260813092223	\N	\N	\N	1
143	F	3	事業所名	Sheet1	B7	20260813092223	\N	20260813092223	\N	\N	\N	1
144	F	3	担当者名	Sheet1	D7	20260813092223	\N	20260813092223	\N	\N	\N	1
145	F	3	担当（主）	Sheet1	B8	20260813092223	\N	20260813092223	\N	\N	\N	1
146	F	3	担当（副）	Sheet1	D8	20260813092223	\N	20260813092223	\N	\N	\N	1
147	F	3	概要	Sheet1	B9	20260813092223	\N	20260813092223	\N	\N	\N	1
148	F	3	内容	Sheet1	B10	20260813092223	\N	20260813092223	\N	\N	\N	1
149	G-8	3	様式	Sheet1	B2	20260813092223	\N	20260813092223	\N	\N	\N	1
150	G-8	3	報告書番号	Sheet1	F2	20260813092223	\N	20260813092223	\N	\N	\N	1
151	G-8	3	都道府県連	Sheet1	B3	20260813092223	\N	20260813092223	\N	\N	\N	1
152	G-8	3	商工会	Sheet1	B4	20260813092223	\N	20260813092223	\N	\N	\N	1
153	G-8	3	実施日	Sheet1	B5	20260813092223	\N	20260813092223	\N	\N	\N	1
154	G-8	3	開始時刻	Sheet1	D5	20260813092223	\N	20260813092223	\N	\N	\N	1
155	G-8	3	終了時刻	Sheet1	F5	20260813092223	\N	20260813092223	\N	\N	\N	1
156	G-8	3	支援テーマ	Sheet1	B6	20260813092223	\N	20260813092223	\N	\N	\N	1
157	G-8	3	業種	Sheet1	D6	20260813092223	\N	20260813092223	\N	\N	\N	1
158	G-8	3	事業所名	Sheet1	B7	20260813092223	\N	20260813092223	\N	\N	\N	1
159	G-8	3	担当者名	Sheet1	D7	20260813092223	\N	20260813092223	\N	\N	\N	1
160	G-8	3	担当（主）	Sheet1	B8	20260813092223	\N	20260813092223	\N	\N	\N	1
161	G-8	3	担当（副）	Sheet1	D8	20260813092223	\N	20260813092223	\N	\N	\N	1
162	G-8	3	概要	Sheet1	B9	20260813092223	\N	20260813092223	\N	\N	\N	1
163	G-8	3	内容	Sheet1	B10	20260813092223	\N	20260813092223	\N	\N	\N	1
164	H	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
165	H	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
166	H	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
167	H	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
168	H	3	年間支援件数	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
169	H	3	年間AI活用件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
170	H	3	最多支援テーマ	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
171	H	3	最多支援テーマ件数	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
172	I-1	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
173	I-1	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
174	I-1	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
175	I-1	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
176	I-1	3	年間支援件数	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
177	I-1	3	年間AI活用件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
178	I-1	3	最多支援テーマ	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
179	I-1	3	最多支援テーマ件数	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
180	I-6	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
181	I-6	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
182	I-6	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
183	I-6	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
184	I-6	3	年間支援件数	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
185	I-6	3	年間AI活用件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
186	I-6	3	最多支援テーマ	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
187	I-6	3	最多支援テーマ件数	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
188	I-7	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
189	I-7	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
190	I-7	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
191	I-7	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
192	I-7	3	年間支援件数	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
193	I-7	3	年間AI活用件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
194	I-7	3	最多支援テーマ	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
195	I-7	3	最多支援テーマ件数	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
196	I-8	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
197	I-8	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
198	I-8	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
199	I-8	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
200	I-8	3	年間支援件数	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
201	I-8	3	年間AI活用件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
202	I-8	3	最多支援テーマ	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
203	I-8	3	最多支援テーマ件数	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
204	I-2	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
205	I-2	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
206	I-2	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
207	I-2	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
208	I-2	3	対象年月	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
209	I-2	3	月間支援件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
210	I-2	3	月間AI活用件数	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
211	I-2	3	最多支援テーマ	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
212	I-2	3	最多支援テーマ件数	Sheet1	B6	20260827133248	\N	20260827133248	\N	\N	\N	1
213	I-3	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
214	I-3	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
215	I-3	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
216	I-3	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
217	I-3	3	対象年月	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
218	I-3	3	月間支援件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
219	I-3	3	月間AI活用件数	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
220	I-3	3	最多支援テーマ	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
221	I-3	3	最多支援テーマ件数	Sheet1	B6	20260827133248	\N	20260827133248	\N	\N	\N	1
222	I-4	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
223	I-4	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
224	I-4	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
225	I-4	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
226	I-4	3	対象年月	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
227	I-4	3	月間支援件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
228	I-4	3	月間AI活用件数	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
229	I-4	3	最多支援テーマ	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
230	I-4	3	最多支援テーマ件数	Sheet1	B6	20260827133248	\N	20260827133248	\N	\N	\N	1
231	I-5	3	様式	Sheet1	B2	20260827133248	\N	20260827133248	\N	\N	\N	1
232	I-5	3	対象年度	Sheet1	E2	20260827133248	\N	20260827133248	\N	\N	\N	1
233	I-5	3	都道府県連	Sheet1	B3	20260827133248	\N	20260827133248	\N	\N	\N	1
234	I-5	3	商工会	Sheet1	E3	20260827133248	\N	20260827133248	\N	\N	\N	1
235	I-5	3	対象年月	Sheet1	B4	20260827133248	\N	20260827133248	\N	\N	\N	1
236	I-5	3	月間支援件数	Sheet1	E4	20260827133248	\N	20260827133248	\N	\N	\N	1
237	I-5	3	月間AI活用件数	Sheet1	B5	20260827133248	\N	20260827133248	\N	\N	\N	1
238	I-5	3	最多支援テーマ	Sheet1	E5	20260827133248	\N	20260827133248	\N	\N	\N	1
239	I-5	3	最多支援テーマ件数	Sheet1	B6	20260827133248	\N	20260827133248	\N	\N	\N	1
\.


--
-- Data for Name: cfg_excel_report_definition; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cfg_excel_report_definition (form_code, fiscal_year_id, template_filename, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by, view_name, is_day_batch) FROM stdin;
G-2	3	report_g2_daybatch_template.xlsx	20260813065853	\N	20260813065853	\N	\N	\N	v_output_g2_excel	t
G-5	3	report_g5_daybatch_template.xlsx	20260813065853	\N	20260813065853	\N	\N	\N	v_output_g5_excel	t
G-3	3	report_g3_template.xlsx	20260813065853	\N	20260813065853	\N	\N	\N	v_output_g3_excel	f
G-4	3	report_g4_template.xlsx	20260813065853	\N	20260813065853	\N	\N	\N	v_output_g4_excel	f
G-6	3	report_g6_template.xlsx	20260813065853	\N	20260813065853	\N	\N	\N	v_output_g6_excel	f
G-7	3	report_g7_template.xlsx	20260813065853	\N	20260813065853	\N	\N	\N	v_output_g7_excel	f
F	3	report_f_template.xlsx	20260813092223	\N	20260813092223	\N	\N	\N	v_output_f_excel	f
G-8	3	report_g8_template.xlsx	20260813092223	\N	20260813092223	\N	\N	\N	v_output_g8_excel	f
H	3	report_h_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_h_excel	f
I-1	3	report_i1_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i1_excel	f
I-6	3	report_i6_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i6_excel	f
I-7	3	report_i7_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i7_excel	f
I-8	3	report_i8_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i8_excel	f
I-2	3	report_i2_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i2_excel	f
I-3	3	report_i3_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i3_excel	f
I-4	3	report_i4_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i4_excel	f
I-5	3	report_i5_template.xlsx	20260827133248	\N	20260827133248	\N	\N	\N	v_output_i5_excel	f
\.


--
-- Data for Name: cfg_menu_item; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cfg_menu_item (role_code, section_sort_order, sort_order, section_label, label, icon, screen_id, default_form, requires_capability, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by, subtitle) FROM stdin;
shokokai	2	0	報告書を見る	報告書を見る	📋	reports	全様式	\N	20260817075135	\N	20260817075135	\N	\N	\N	\N
shokokai	5	0	管理	アカウント管理	⚙️	accounts	\N	can_manage_own_account	20260817075135	\N	20260817075135	\N	\N	\N	\N
shokokai	0	0	ホーム	ホーム	🏠	dashboard	\N	\N	20260817075135	\N	20260817075135	\N	\N	\N	事業環境変化対応型支援事業
shokokai	1	0	受付／報告書を作成する	相談を受ける	🗣️	ai-input	\N	can_edit_reports	20260817075135	\N	20260817075135	\N	\N	\N	\N
shokokai	1	1	受付／報告書を作成する	報告書を作る	✍️	manual-input	\N	can_edit_reports	20260817075135	\N	20260817075135	\N	\N	\N	\N
shokokai	1	2	受付／報告書を作成する	専門家の報告を取り込む	📥	expert-import	\N	can_edit_reports	20260817075135	\N	20260817075135	\N	\N	\N	\N
shokokai	3	0	実績確認・帳票出力	実績確認・帳票出力	📈	monthly	\N	\N	20260826222648	\N	20260826222648	\N	\N	\N	\N
shokokai	4	1	AI支援提案	ナレッジを検索する	🔍	ai-proposal	search	\N	20260817075135	\N	20260817075135	\N	\N	\N	\N
shokokai	4	0	AI支援提案	AIに相談する	🧑‍💻💭	ai-proposal	proposal	\N	20260817075135	\N	20260817075135	\N	\N	\N	\N
zenkoku	4	0	管理	アカウント管理	⚙️	accounts	\N	can_manage_accounts	20260808115851	\N	20260808115851	\N	\N	\N	\N
zenkoku	4	1	管理	ナレッジ管理	🧠	knowledge	\N	can_manage_knowledge	20260808115851	\N	20260808115851	\N	\N	\N	\N
zenkoku	3	0	AI支援提案	AIに相談する	🧑‍💻💭	ai-proposal	proposal	\N	20260826225616	\N	20260826225616	\N	\N	\N	\N
zenkoku	3	1	AI支援提案	ナレッジを検索する	🔍	ai-proposal	search	\N	20260826225616	\N	20260826225616	\N	\N	\N	\N
zenkoku	2	0	実績確認・帳票出力	実績確認・帳票出力	📈	monthly	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	\N
zenkoku	1	0	報告書を見る	報告書を見る	📋	reports	全様式	\N	20260808115851	\N	20260808115851	\N	\N	\N	\N
zenkoku	0	0	ホーム	ホーム	📊	dashboard	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	事業環境変化対応型支援事業
ken	5	0	管理	アカウント管理	🏢	accounts	\N	can_manage_shokokai	20260808115851	\N	20260808115851	\N	\N	\N	\N
ken	5	1	管理	ナレッジ管理	🧠	knowledge	\N	can_manage_knowledge	20260808115851	\N	20260808115851	\N	\N	\N	\N
ken	4	0	AI支援提案	AIに相談する	🧑‍💻💭	ai-proposal	proposal	\N	20260826225559	\N	20260826225559	\N	\N	\N	\N
ken	4	1	AI支援提案	ナレッジを検索する	🔍	ai-proposal	search	\N	20260826225559	\N	20260826225559	\N	\N	\N	\N
ken	3	0	実績確認・帳票出力	実績確認・帳票出力	📈	monthly	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	\N
ken	1	0	報告書を見る	報告書を見る	📋	reports	全様式	\N	20260808115851	\N	20260808115851	\N	\N	\N	\N
ken	0	0	ホーム	ホーム	📊	dashboard	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	事業環境変化対応型支援事業
\.


--
-- Data for Name: cfg_rag_setting; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cfg_rag_setting (rag_setting_id, embedding_model, vector_db, chunk_size, chunk_overlap, last_synced_at, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	text-embedding-3-large	pgvector	800	100	2026-08-09 00:34:57.739862+09	20260808115851	\N	20260809003457	1	\N	\N
\.


--
-- Data for Name: cfg_system_setting; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cfg_system_setting (setting_code, label, setting_value, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
national_prefecture_code	全国連の県コード	00	20260808115851	\N	20260808115851	\N	\N	\N
voice_input_default_minutes	音声入力の最大録音時間（分）	30	20260808115851	\N	20260808115851	\N	\N	\N
federation_shokokai_cd	連合会のコード	0021	20260808115851	\N	20260808115851	\N	\N	\N
max_failed_login_attempts	ログイン失敗によるアカウントロックまでの回数	5	20260808115851	\N	20260808115851	\N	\N	\N
lockout_minutes	アカウントロックの継続時間（分）	15	20260808115851	\N	20260808115851	\N	\N	\N
report_list_limit	報告書一覧が1回で取得する最大件数	100	20260808115851	\N	20260808115851	\N	\N	\N
account_list_limit	アカウント一覧が1回で取得する最大件数	100	20260808120313	\N	20260808120313	\N	\N	\N
help_desk_phone	ヘルプデスクの電話番号	00-0000-0000	20260808133457	\N	20260808133457	\N	\N	\N
help_desk_email	ヘルプデスクのメールアドレス	mail-support@xxx-yyyzzz.co.jp	20260808133457	\N	20260808133457	\N	\N	\N
help_desk_hours	ヘルプデスクの受付時間	9:00～17:00	20260808133457	\N	20260808133457	\N	\N	\N
help_desk_closed_days	ヘルプデスクの特別休業日	2026-12-29,2026-12-30,2026-12-31,2027-01-01,2027-01-02,2027-01-03	20260808133457	\N	20260808133457	\N	\N	\N
log_output_categories	ログに出力する項目（カンマ区切り。menu=メニュー選択、file_output=ファイル出力）	menu,file_output	20260809013447	\N	20260809013447	\N	\N	\N
csv_output_filename_pattern	CSV出力ファイル名のパターン（{title}=一覧タイトル、{timestamp}=出力日時yyyymmddhhmmss）	{title}_{timestamp}.csv	20260812150314	\N	20260812150314	\N	\N	\N
excel_output_filename_pattern	Excel帳票出力ファイル名のパターン（{title}=帳票名、{timestamp}=出力日時yyyymmddhhmmss）	output_{title}.xlsx	20260812150314	\N	20260812150314	\N	\N	\N
two_factor_trusted_device_days	2段階認証の端末認証許可日数	1	20260808115851	\N	20260808115851	\N	\N	\N
voice_input_max_minutes	音声入力タイマーの上限時間（分）	60	20260827122808	\N	20260827122808	\N	\N	\N
voice_input_extend_minutes	音声入力タイマーの1回あたり延長時間（分）	30	20260827122808	\N	20260827122808	\N	\N	\N
\.


--
-- Data for Name: mst_capital_range; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_capital_range (capital_range_id, fiscal_year_id, capital_range_code, label, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	3	c1	500万円以下	1	20260813065853	\N	20260813065853	\N	\N	\N
2	3	c2	500万円超1000万円以下	2	20260813065853	\N	20260813065853	\N	\N	\N
3	3	c3	1000万円超3000万円以下	3	20260813065853	\N	20260813065853	\N	\N	\N
4	3	c4	3000万円超	4	20260813065853	\N	20260813065853	\N	\N	\N
\.


--
-- Data for Name: mst_employee_range; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_employee_range (employee_range_id, fiscal_year_id, employee_range_code, label, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	3	e1	5人以下	1	20260813065853	\N	20260813065853	\N	\N	\N
2	3	e2	6人以上20人以下	2	20260813065853	\N	20260813065853	\N	\N	\N
3	3	e3	21人以上50人以下	3	20260813065853	\N	20260813065853	\N	\N	\N
4	3	e4	51人以上	4	20260813065853	\N	20260813065853	\N	\N	\N
\.


--
-- Data for Name: mst_fiscal_year; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_fiscal_year (fiscal_year_id, fiscal_year_code, label, start_month, end_month, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by, stat_as_of_date) FROM stdin;
1	R6	令和6年度	2024-02	2025-02	20260808115851	\N	20260808115851	\N	\N	\N	\N
2	R7	令和7年度	2025-02	2026-02	20260808115851	\N	20260808115851	\N	\N	\N	2026-01-01
3	R8	令和8年度	2026-02	2027-02	20260808115851	\N	20260808115851	\N	\N	\N	2026-08-01
\.


--
-- Data for Name: mst_form; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_form (form_code, fiscal_year_id, short_label, full_label, badge_class, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
H	1	H 月次総支援件数	H 月次実績報告総支援件数	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-1	1	I-1 相談員等配置状況	I-1 月次実績報告相談員等配置状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-2	1	I-2 月次相談員（人件費、雑役務費）	I-2 月次実績報告相談員（人件費、雑役務費）	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-3	1	I-3 月次相談員（謝金）	I-3 月次実績報告相談員（謝金）支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-4	1	I-4 月次専門家・相談会支援状況	I-4 月次実績報告専門家派遣・個人相談会支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-5	1	I-5 月次普及員支援	I-5 月次実績報告施策普及員支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-6	1	I-6 月次講習会状況	I-6 月次実績報告事業者向け講習会実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-7	1	I-7 月次研修会状況	I-7 月次実績報告経営指導員等向け研修会実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-8	1	I-8 月次地方紙広告掲載	I-8 月次実績報告地方紙広告掲載実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
H	2	H 月次総支援件数	H 月次実績報告総支援件数	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-1	2	I-1 相談員等配置状況	I-1 月次実績報告相談員等配置状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-2	2	I-2 月次相談員（人件費、雑役務費）	I-2 月次実績報告相談員（人件費、雑役務費）	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-3	2	I-3 月次相談員（謝金）	I-3 月次実績報告相談員（謝金）支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-4	2	I-4 月次専門家・相談会支援状況	I-4 月次実績報告専門家派遣・個人相談会支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-5	2	I-5 月次普及員支援	I-5 月次実績報告施策普及員支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-6	2	I-6 月次講習会状況	I-6 月次実績報告事業者向け講習会実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-7	2	I-7 月次研修会状況	I-7 月次実績報告経営指導員等向け研修会実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-8	2	I-8 月次地方紙広告掲載	I-8 月次実績報告地方紙広告掲載実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
H	3	H 月次総支援件数	H 月次実績報告総支援件数	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-1	3	I-1 相談員等配置状況	I-1 月次実績報告相談員等配置状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-2	3	I-2 月次相談員（人件費、雑役務費）	I-2 月次実績報告相談員（人件費、雑役務費）	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-3	3	I-3 月次相談員（謝金）	I-3 月次実績報告相談員（謝金）支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-4	3	I-4 月次専門家・相談会支援状況	I-4 月次実績報告専門家派遣・個人相談会支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-5	3	I-5 月次普及員支援	I-5 月次実績報告施策普及員支援状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-6	3	I-6 月次講習会状況	I-6 月次実績報告事業者向け講習会実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-7	3	I-7 月次研修会状況	I-7 月次実績報告経営指導員等向け研修会実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
I-8	3	I-8 月次地方紙広告掲載	I-8 月次実績報告地方紙広告掲載実施状況	\N	20260808115851	\N	20260808115851	\N	\N	\N
F	3	F 相談受付	F 相談受付票	#a04020	20260808115851	\N	20260808115851	\N	\N	\N
G-2	3	G-2 専門家相談員	G-2 専門家相談員報告書	#1a6fa8	20260808115851	\N	20260808115851	\N	\N	\N
G-3	3	G-3 講習会	G-3 事業者向け講習会報告書	#1a7a4a	20260808115851	\N	20260808115851	\N	\N	\N
G-4	3	G-4 専門家派遣	G-4 専門家派遣報告書	#5b3fa0	20260808115851	\N	20260808115851	\N	\N	\N
G-5	3	G-5 個人相談会	G-5 個人相談会報告書	#8b5e10	20260808115851	\N	20260808115851	\N	\N	\N
G-6	3	G-6 研修会	G-6 指導員等研修会報告書	#a02020	20260808115851	\N	20260808115851	\N	\N	\N
G-7	3	G-7 施策普及員	G-7 施策普及員報告書	#2050a0	20260808115851	\N	20260808115851	\N	\N	\N
G-8	3	G-8 研修会実績	G-8 研修会実績報告書	#1d6a6a	20260808115851	\N	20260808115851	\N	\N	\N
\.


--
-- Data for Name: mst_industry; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_industry (industry_code, fiscal_year_id, label, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
I	3	卸売業、小売業	1	20260808115851	\N	20260808115851	\N	\N	\N
R	3	サービス業（他に分類されないもの）	2	20260808115851	\N	20260808115851	\N	\N	\N
D	3	建設業	3	20260808115851	\N	20260808115851	\N	\N	\N
M	3	宿泊業、飲食サービス業	4	20260808115851	\N	20260808115851	\N	\N	\N
P	3	医療、福祉	5	20260808115851	\N	20260808115851	\N	\N	\N
E	3	製造業	6	20260808115851	\N	20260808115851	\N	\N	\N
N	3	生活関連サービス業、娯楽業	7	20260808115851	\N	20260808115851	\N	\N	\N
K	3	不動産業、物品賃貸業	8	20260808115851	\N	20260808115851	\N	\N	\N
H	3	運輸業、郵便業	9	20260808115851	\N	20260808115851	\N	\N	\N
L	3	学術研究、専門・技術サービス業	10	20260808115851	\N	20260808115851	\N	\N	\N
O	3	教育、学習支援業	11	20260808115851	\N	20260808115851	\N	\N	\N
G	3	情報通信業	12	20260808115851	\N	20260808115851	\N	\N	\N
J	3	金融業、保険業	13	20260808115851	\N	20260808115851	\N	\N	\N
F	3	電気・ガス・熱供給・水道業	14	20260808115851	\N	20260808115851	\N	\N	\N
A	3	農業、林業	15	20260808115851	\N	20260808115851	\N	\N	\N
Q	3	複合サービス事業	16	20260808115851	\N	20260808115851	\N	\N	\N
B	3	漁業	17	20260808115851	\N	20260808115851	\N	\N	\N
C	3	鉱業、採石業、砂利採取業	18	20260808115851	\N	20260808115851	\N	\N	\N
S	3	公務（他に分類されるものを除く）	19	20260808115851	\N	20260808115851	\N	\N	\N
T	3	分類不能の産業	20	20260808115851	\N	20260808115851	\N	\N	\N
\.


--
-- Data for Name: mst_prefecture; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_prefecture (prefecture_code, name, short_name, region, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
00	全国連	全国連	\N	0	20260808115851	\N	20260808115851	\N	\N	\N
01	北海道	北海道	hokkaido	1	20260808115851	\N	20260808115851	\N	\N	\N
02	青森県	青森	tohoku	2	20260808115851	\N	20260808115851	\N	\N	\N
03	岩手県	岩手	tohoku	3	20260808115851	\N	20260808115851	\N	\N	\N
04	宮城県	宮城	tohoku	4	20260808115851	\N	20260808115851	\N	\N	\N
05	秋田県	秋田	tohoku	5	20260808115851	\N	20260808115851	\N	\N	\N
06	山形県	山形	tohoku	6	20260808115851	\N	20260808115851	\N	\N	\N
07	福島県	福島	tohoku	7	20260808115851	\N	20260808115851	\N	\N	\N
08	茨城県	茨城	kanto	8	20260808115851	\N	20260808115851	\N	\N	\N
09	栃木県	栃木	kanto	9	20260808115851	\N	20260808115851	\N	\N	\N
10	群馬県	群馬	kanto	10	20260808115851	\N	20260808115851	\N	\N	\N
11	埼玉県	埼玉	kanto	11	20260808115851	\N	20260808115851	\N	\N	\N
12	千葉県	千葉	kanto	12	20260808115851	\N	20260808115851	\N	\N	\N
13	東京都	東京	kanto	13	20260808115851	\N	20260808115851	\N	\N	\N
14	神奈川県	神奈川	kanto	14	20260808115851	\N	20260808115851	\N	\N	\N
15	新潟県	新潟	chubu	15	20260808115851	\N	20260808115851	\N	\N	\N
16	富山県	富山	chubu	16	20260808115851	\N	20260808115851	\N	\N	\N
17	石川県	石川	chubu	17	20260808115851	\N	20260808115851	\N	\N	\N
18	福井県	福井	chubu	18	20260808115851	\N	20260808115851	\N	\N	\N
19	山梨県	山梨	chubu	19	20260808115851	\N	20260808115851	\N	\N	\N
20	長野県	長野	chubu	20	20260808115851	\N	20260808115851	\N	\N	\N
21	岐阜県	岐阜	chubu	21	20260808115851	\N	20260808115851	\N	\N	\N
22	静岡県	静岡	chubu	22	20260808115851	\N	20260808115851	\N	\N	\N
23	愛知県	愛知	chubu	23	20260808115851	\N	20260808115851	\N	\N	\N
24	三重県	三重	kinki	24	20260808115851	\N	20260808115851	\N	\N	\N
25	滋賀県	滋賀	kinki	25	20260808115851	\N	20260808115851	\N	\N	\N
26	京都府	京都	kinki	26	20260808115851	\N	20260808115851	\N	\N	\N
27	大阪府	大阪	kinki	27	20260808115851	\N	20260808115851	\N	\N	\N
28	兵庫県	兵庫	kinki	28	20260808115851	\N	20260808115851	\N	\N	\N
29	奈良県	奈良	kinki	29	20260808115851	\N	20260808115851	\N	\N	\N
30	和歌山県	和歌山	kinki	30	20260808115851	\N	20260808115851	\N	\N	\N
31	鳥取県	鳥取	chugoku	31	20260808115851	\N	20260808115851	\N	\N	\N
32	島根県	島根	chugoku	32	20260808115851	\N	20260808115851	\N	\N	\N
33	岡山県	岡山	chugoku	33	20260808115851	\N	20260808115851	\N	\N	\N
34	広島県	広島	chugoku	34	20260808115851	\N	20260808115851	\N	\N	\N
35	山口県	山口	chugoku	35	20260808115851	\N	20260808115851	\N	\N	\N
36	徳島県	徳島	shikoku	36	20260808115851	\N	20260808115851	\N	\N	\N
37	香川県	香川	shikoku	37	20260808115851	\N	20260808115851	\N	\N	\N
38	愛媛県	愛媛	shikoku	38	20260808115851	\N	20260808115851	\N	\N	\N
39	高知県	高知	shikoku	39	20260808115851	\N	20260808115851	\N	\N	\N
40	福岡県	福岡	kyushu	40	20260808115851	\N	20260808115851	\N	\N	\N
41	佐賀県	佐賀	kyushu	41	20260808115851	\N	20260808115851	\N	\N	\N
42	長崎県	長崎	kyushu	42	20260808115851	\N	20260808115851	\N	\N	\N
43	熊本県	熊本	kyushu	43	20260808115851	\N	20260808115851	\N	\N	\N
44	大分県	大分	kyushu	44	20260808115851	\N	20260808115851	\N	\N	\N
45	宮崎県	宮崎	kyushu	45	20260808115851	\N	20260808115851	\N	\N	\N
46	鹿児島県	鹿児島	kyushu	46	20260808115851	\N	20260808115851	\N	\N	\N
47	沖縄県	沖縄	kyushu	47	20260808115851	\N	20260808115851	\N	\N	\N
\.


--
-- Data for Name: mst_qualification; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_qualification (qualification_id, fiscal_year_id, qualification_code, label, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	3	sme_consultant	中小企業診断士	1	20260812195055	\N	20260812195055	\N	\N	\N
2	3	labor_consultant	社会保険労務士	2	20260812195055	\N	20260812195055	\N	\N	\N
\.


--
-- Data for Name: mst_revenue_range; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_revenue_range (revenue_range_id, fiscal_year_id, revenue_range_code, label, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	3	r1	1000万円以下	1	20260813065853	\N	20260813065853	\N	\N	\N
2	3	r2	1000万円超5000万円以下	2	20260813065853	\N	20260813065853	\N	\N	\N
3	3	r3	5000万円超1億円以下	3	20260813065853	\N	20260813065853	\N	\N	\N
4	3	r4	1億円超	4	20260813065853	\N	20260813065853	\N	\N	\N
\.


--
-- Data for Name: mst_shokokai; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_shokokai (prefecture_code, shokokai_cd, name, sort_order, group_code, group_label, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by, short_name) FROM stdin;
00	0021	全国商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	全国連合会
01	0021	北海道商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	北海道連合会
01	2001	石狩北商工会	0	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	石狩北
01	2002	北広島商工会	1	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	北広島
01	2003	当別町商工会	2	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	当別町
01	2004	新篠津村商工会	3	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	新篠津村
01	2005	函館東商工会	4	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	函館東
01	2006	函館市亀田商工会	5	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	函館市亀田
01	2007	北斗市商工会	6	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	北斗市
01	2008	松前商工会	7	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	松前
01	2009	福島町商工会	8	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	福島町
01	2010	知内商工会	9	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	知内
01	2011	木古内商工会	10	1	石狩	20260808115851	\N	20260808115851	\N	\N	\N	木古内
01	2012	七飯町商工会	11	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	七飯町
01	2013	鹿部商工会	12	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	鹿部
01	2014	森町さわら商工会	13	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	森町さわら
01	2015	八雲商工会	14	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	八雲
01	2016	長万部商工会	15	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	長万部
01	2017	江差商工会	16	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	江差
01	2018	上ノ国町商工会	17	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	上ノ国町
01	2019	厚沢部商工会	18	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	厚沢部
01	2020	乙部町商工会	19	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	乙部町
01	2021	奥尻商工会	20	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	奥尻
01	2022	今金町商工会	21	2	渡島	20260808115851	\N	20260808115851	\N	\N	\N	今金町
01	2023	せたな商工会	22	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	せたな
01	2024	島牧商工会	23	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	島牧
01	2025	寿都商工会	24	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	寿都
01	2026	黒松内町商工会	25	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	黒松内町
01	2027	蘭越町商工会	26	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	蘭越町
01	2028	ニセコ町商工会	27	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	ニセコ町
01	2029	真狩村商工会	28	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	真狩村
01	2030	留寿都商工会	29	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	留寿都
01	2031	喜茂別町商工会	30	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	喜茂別町
01	2032	京極町商工会	31	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	京極町
01	2033	共和町商工会	32	3	檜山	20260808115851	\N	20260808115851	\N	\N	\N	共和町
01	2034	泊村商工会	33	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	泊村
01	2035	神恵内村商工会	34	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	神恵内村
01	2036	積丹町商工会	35	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	積丹町
01	2037	古平町商工会	36	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	古平町
01	2038	仁木町商工会	37	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	仁木町
01	2039	赤井川村商工会	38	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	赤井川村
01	2040	いわみざわ商工会	39	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	いわみざわ
01	2041	三笠市商工会	40	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	三笠市
01	2042	江部乙商工会	41	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	江部乙
01	2043	南幌町商工会	42	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	南幌町
01	2044	奈井江町商工会	43	4	後志	20260808115851	\N	20260808115851	\N	\N	\N	奈井江町
01	2045	由仁町商工会	44	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	由仁町
01	2046	長沼町商工会	45	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	長沼町
01	2047	月形商工会	46	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	月形
01	2048	浦臼町商工会	47	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	浦臼町
01	2049	新十津川町商工会	48	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	新十津川町
01	2050	妹背牛商工会	49	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	妹背牛
01	2051	秩父別町商工会	50	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	秩父別町
01	2052	雨竜町商工会	51	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	雨竜町
01	2053	北竜町商工会	52	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	北竜町
01	2054	沼田町商工会	53	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	沼田町
01	2055	あさひかわ商工会	54	5	空知	20260808115851	\N	20260808115851	\N	\N	\N	あさひかわ
01	2056	山部商工会	55	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	山部
01	2057	鷹栖町商工会	56	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	鷹栖町
01	2058	東神楽町商工会	57	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	東神楽町
01	2059	当麻町商工会	58	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	当麻町
01	2060	比布商工会	59	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	比布
01	2061	愛別商工会	60	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	愛別
01	2062	上川町商工会	61	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	上川町
01	2063	東川町商工会	62	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	東川町
01	2064	美瑛町商工会	63	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	美瑛町
01	2065	上富良野町商工会	64	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	上富良野町
01	2066	中富良野町商工会	65	6	上川	20260808115851	\N	20260808115851	\N	\N	\N	中富良野町
01	2067	南富良野町商工会	66	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	南富良野町
01	2068	占冠村商工会	67	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	占冠村
01	2069	和寒町商工会	68	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	和寒町
01	2070	剣渕商工会	69	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	剣渕
01	2071	朝日商工会	70	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	朝日
01	2072	風連商工会	71	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	風連
01	2073	下川町商工会	72	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	下川町
01	2074	美深町商工会	73	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	美深町
01	2075	音威子府村商工会	74	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	音威子府村
01	2076	中川町商工会	75	7	留萌	20260808115851	\N	20260808115851	\N	\N	\N	中川町
01	2077	幌加内町商工会	76	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	幌加内町
01	2078	増毛町商工会	77	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	増毛町
01	2079	小平町商工会	78	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	小平町
01	2080	苫前町商工会	79	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	苫前町
01	2081	羽幌町商工会	80	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	羽幌町
01	2082	初山別村商工会	81	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	初山別村
01	2083	遠別商工会	82	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	遠別
01	2084	天塩商工会	83	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	天塩
01	2085	幌延町商工会	84	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	幌延町
01	2086	猿払村商工会	85	8	宗谷	20260808115851	\N	20260808115851	\N	\N	\N	猿払村
01	2087	浜頓別町商工会	86	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	浜頓別町
01	2088	中頓別町商工会	87	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	中頓別町
01	2089	枝幸町商工会	88	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	枝幸町
01	2090	豊富町商工会	89	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	豊富町
01	2091	礼文町商工会	90	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	礼文町
01	2092	利尻町商工会	91	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	利尻町
01	2093	利尻富士町商工会	92	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	利尻富士町
01	2094	きたみ市商工会	93	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	きたみ市
01	2095	津別町商工会	94	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	津別町
01	2096	斜里町商工会	95	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	斜里町
01	2097	清里町商工会	96	9	オホーツク	20260808115851	\N	20260808115851	\N	\N	\N	清里町
01	2098	小清水町商工会	97	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	小清水町
01	2099	訓子府町商工会	98	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	訓子府町
01	2100	置戸町商工会	99	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	置戸町
01	2101	佐呂間町商工会	100	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	佐呂間町
01	2102	えんがる商工会	101	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	えんがる
01	2103	湧別町商工会	102	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	湧別町
01	2104	滝上町商工会	103	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	滝上町
01	2105	興部町商工会	104	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	興部町
01	2106	西興部村商工会	105	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	西興部村
01	2107	雄武町商工会	106	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	雄武町
01	2108	大空町商工会	107	10	十勝	20260808115851	\N	20260808115851	\N	\N	\N	大空町
01	2109	豊浦町商工会	108	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	豊浦町
01	2110	壮瞥町商工会	109	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	壮瞥町
01	2111	白老町商工会	110	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	白老町
01	2112	厚真町商工会	111	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	厚真町
01	2113	洞爺湖町商工会	112	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	洞爺湖町
01	2114	安平町商工会	113	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	安平町
01	2115	むかわ町商工会	114	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	むかわ町
01	2116	日高町商工会	115	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	日高町
01	2117	平取町商工会	116	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	平取町
01	2118	新冠町商工会	117	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	新冠町
01	2119	様似町商工会	118	11	釧路	20260808115851	\N	20260808115851	\N	\N	\N	様似町
01	2120	えりも町商工会	119	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	えりも町
01	2121	新ひだか町商工会	120	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	新ひだか町
01	2122	音更町商工会	121	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	音更町
01	2123	士幌町商工会	122	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	士幌町
01	2124	上士幌町商工会	123	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	上士幌町
01	2125	鹿追町商工会	124	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	鹿追町
01	2126	新得町商工会	125	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	新得町
01	2127	清水町商工会	126	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	清水町
01	2128	芽室町商工会	127	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	芽室町
01	2129	中札内村商工会	128	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	中札内村
01	2130	更別村商工会	129	12	根室	20260808115851	\N	20260808115851	\N	\N	\N	更別村
01	2131	大樹町商工会	130	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	大樹町
01	2132	広尾町商工会	131	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	広尾町
01	2133	幕別町商工会	132	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	幕別町
01	2134	池田町商工会	133	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	池田町
01	2135	豊頃町商工会	134	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	豊頃町
01	2136	本別町商工会	135	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	本別町
01	2137	足寄町商工会	136	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	足寄町
01	2138	陸別町商工会	137	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	陸別町
01	2139	浦幌町商工会	138	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	浦幌町
01	2140	釧路町商工会	139	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	釧路町
01	2141	厚岸町商工会	140	13	胆振	20260808115851	\N	20260808115851	\N	\N	\N	厚岸町
01	2142	浜中町商工会	141	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	浜中町
01	2143	標茶町商工会	142	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	標茶町
01	2144	弟子屈町商工会	143	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	弟子屈町
01	2145	阿寒町商工会	144	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	阿寒町
01	2146	鶴居村商工会	145	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	鶴居村
01	2147	白糠町商工会	146	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	白糠町
01	2148	音別町商工会	147	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	音別町
01	2149	別海町商工会	148	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	別海町
01	2150	中標津町商工会	149	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	中標津町
01	2151	標津町商工会	150	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	標津町
01	2152	羅臼町商工会	151	14	日高	20260808115851	\N	20260808115851	\N	\N	\N	羅臼町
02	0021	青森県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	青森県連合会
02	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
02	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
02	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
03	0021	岩手県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	岩手県連合会
03	2001	△△商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
03	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
03	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
04	0021	宮城県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	宮城県連合会
04	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
04	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
04	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
05	0021	秋田県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	秋田県連合会
05	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
05	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
05	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
06	0021	山形県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	山形県連合会
06	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
06	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
06	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
07	0021	福島県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	福島県連合会
07	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
07	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
07	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
08	0021	茨城県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	茨城県連合会
08	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
08	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
08	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
09	0021	栃木県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	栃木県連合会
09	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
09	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
09	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
10	0021	群馬県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	群馬県連合会
10	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
10	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
10	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
11	0021	埼玉県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	埼玉県連合会
11	2001	△△商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
11	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
11	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
12	0021	千葉県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	千葉県連合会
12	2001	■■商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	■■
12	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
12	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
13	0021	東京都商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	東京都連合会
13	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
13	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
13	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
14	0021	神奈川県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	神奈川県連合会
14	2001	□□商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
14	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
14	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
15	0021	新潟県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	新潟県連合会
15	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
15	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
15	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
16	0021	富山県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	富山県連合会
16	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
16	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
16	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
17	0021	石川県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	石川県連合会
17	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
17	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
17	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
18	0021	福井県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	福井県連合会
18	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
18	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
18	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
19	0021	山梨県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	山梨県連合会
19	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
19	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
19	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
20	0021	長野県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	長野県連合会
20	2001	南箕輪村商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	南箕輪村
20	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
20	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
21	0021	岐阜県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	岐阜県連合会
21	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
21	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
21	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
22	0021	静岡県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	静岡県連合会
22	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
22	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
22	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
23	0021	愛知県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	愛知県連合会
23	2001	△△商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
23	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
23	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
24	0021	三重県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	三重県連合会
24	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
24	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
24	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
25	0021	滋賀県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	滋賀県連合会
25	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
25	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
25	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
26	0021	京都府商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	京都府連合会
26	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
26	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
26	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
27	0021	大阪府商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	大阪府連合会
27	2001	□□商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
27	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
27	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
28	0021	兵庫県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	兵庫県連合会
28	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
28	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
28	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
29	0021	奈良県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	奈良県連合会
29	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
29	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
29	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
30	0021	和歌山県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	和歌山県連合会
30	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
30	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
30	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
31	0021	鳥取県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	鳥取県連合会
31	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
31	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
31	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
32	0021	島根県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	島根県連合会
32	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
32	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
32	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
33	0021	岡山県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	岡山県連合会
33	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
33	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
33	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
34	0021	広島県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	広島県連合会
34	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
34	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
34	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
35	0021	山口県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	山口県連合会
35	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
35	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
35	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
36	0021	徳島県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	徳島県連合会
36	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
36	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
36	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
37	0021	香川県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	香川県連合会
37	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
37	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
37	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
38	0021	愛媛県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	愛媛県連合会
38	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
38	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
38	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
39	0021	高知県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	高知県連合会
39	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
39	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
39	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
40	0021	福岡県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	福岡県連合会
40	2001	■■商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	■■
40	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
40	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
41	0021	佐賀県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	佐賀県連合会
41	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
41	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
41	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
42	0021	長崎県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	長崎県連合会
42	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
42	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
42	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
43	0021	熊本県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	熊本県連合会
43	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
43	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
43	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
44	0021	大分県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	大分県連合会
44	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
44	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
44	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
45	0021	宮崎県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	宮崎県連合会
45	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
45	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
45	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
46	0021	鹿児島県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	鹿児島県連合会
46	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
46	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
46	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
47	0021	沖縄県商工会連合会	\N	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	沖縄県連合会
47	2001	○○商工会	0	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	○○
47	2002	△△商工会	1	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	△△
47	2003	□□商工会	2	\N	\N	20260808115851	\N	20260808115851	\N	\N	\N	□□
\.


--
-- Data for Name: mst_theme; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_theme (theme_id, fiscal_year_id, theme_code, label, badge_class, group_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
13	3	wage	賃上げ・最低賃金引上げ	#8b5e10	1	20260809010938	\N	20260809010938	\N	\N	\N
14	3	labor	省力化促進・人手不足	#1a7a4a	2	20260809010938	\N	20260809010938	\N	\N	\N
15	3	energy	エネルギー価格・物価の高騰	#1a6fa8	3	20260809010938	\N	20260809010938	\N	\N	\N
16	3	digital	デジタル化	#5b3fa0	4	20260809010938	\N	20260809010938	\N	\N	\N
17	3	tariff	米国関税	#a02020	5	20260809010938	\N	20260809010938	\N	\N	\N
18	3	invoice	インボイス制度	#1d6a6a	6	20260809010938	\N	20260809010938	\N	\N	\N
19	3	ebooks	電子帳簿保存法	#5a6472	7	20260809010938	\N	20260809010938	\N	\N	\N
20	3	covid	新型コロナ	#b5566f	8	20260809010938	\N	20260809010938	\N	\N	\N
21	3	admin	事業実施に係る事務処理	#2d8577	9	20260809010938	\N	20260809010938	\N	\N	\N
\.


--
-- Data for Name: mst_user_account; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_user_account (user_account_id, prefecture_code, shokokai_cd, user_id, shokuin_kj, email, status, core_linked, permission_level, last_login_at, password, totp_secret, is_mfa_enabled, failed_login_count, locked_until, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
6	14	0021	14	神奈川 久美子	kanagawa@example.jp	1	t	一般職員	2026-07-21 04:52:00+09	14	TLGEO7MCPQ4ABFS6SGBC3Q32IBXOEYMK	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
7	20	0021	20	長野 一郎	nagano@example.jp	1	f	一般職員	2026-07-19 03:35:00+09	20	EK26V56UDFLYHNQK4JMNMGET64JW44T4	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
9	27	0021	27	大阪 隆	osaka@example.jp	1	t	一般職員	2026-07-15 01:01:00+09	27	OYC334ZUKXKEYWPAT4M2T2RQSPW3EHHM	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
10	28	0021	28	兵庫 誠	hyogo@example.jp	1	f	一般職員	2026-07-13 00:44:00+09	28	CP435SUGK5WG73PLQS73EJRV6S43DTS6	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
11	40	0021	40	福岡 由美	fukuoka@example.jp	0	f	一般職員	\N	40	HWN77AYHZICPFDBANMSNAABLNNTVGQ3Q	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
17	01	2055	ST-206	渡辺 隆	watanabe@asahikawa.example.jp	1	f	一般職員	2026-07-19 05:45:00+09	ST-206	577JFVAV4CG6BCTHHM4KYBDRCUT7HP3F	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
18	01	2094	ST-207	山本 恵美	yamamoto@kitami.example.jp	1	t	一般職員	2026-07-17 04:28:00+09	ST-207	OYNIDGUFCQ66GQ33EWLBMEDG27JLX5E3	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
19	01	2122	ST-208	中村 誠	nakamura@otofuke.example.jp	1	f	一般職員	2026-07-15 03:11:00+09	ST-208	GOHCJ5YNR234E4APE3GMOSMMRB4NZFQI	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
20	01	2140	ST-209	小林 明	kobayashi@kushiro.example.jp	0	f	一般職員	\N	ST-209	DO4R4CXBYQXJMTUPXBJKWQSZUYE22M47	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
42	31	2002	ST-202	△△商工会担当者	31-st-202@example.jp	1	f	一般職員	\N	ST-202	6G43ESQGCVBX76NVBEPTMOHPUGIT3T2K	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
43	31	2003	ST-203	□□商工会担当者	31-st-203@example.jp	1	f	一般職員	\N	ST-203	36ECKGXVUPMIVH2Q2ZENXW6CDWJ3L6EG	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
21	01	2149	ST-210	加藤 由美	kato@betsukai.example.jp	1	f	一般職員	2026-08-03 12:10:38.747099+09	ST-210	7QYJHHJMVVMHBLEWBD77W5P2EZMD3WUN	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
3	02	0021	02	青森 花子	aomori@example.jp	1	t	県連（商工会権限）	2026-08-07 00:17:54.120822+09	02	O2OJPGU5LQPU4OTRWC7FLHO6KE6LQSBX	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
15	01	2020	ST-204	高橋 久美子	takahashi@otobe.example.jp	1	f	一般職員	2026-08-07 00:33:26.731613+09	ST-204	PT4BUZIOXVDEUCISCKEJ5M4ZSZRBBHVP	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
4	03	0021	03	岩手 次郎	iwate@example.jp	0	f	一般職員	\N	03	QVLRXOSVQMLZA25NZJQOHG7HTJGSGZRX	t	0	\N	20260808115851	\N	20260808121748	1	\N	\N
14	01	2010	ST-203	佐藤 三郎	sato@shiriuchi.example.jp	1	t	一般職員	2026-08-08 14:51:02.266554+09	ST-203	PUGQVSIA2NB3S2UJTRQVJEGVW3L55KQ6	t	0	\N	20260808115851	\N	20260808152639	2	\N	\N
5	13	0021	13	東京 三郎	tokyo@example.jp	1	f	管理者	2026-07-23 05:09:00+09	13	KV2BM252P65R2GXHN5JOTQQUKC2NOVUA	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
12	01	2001	013	高木 修	013@013.013.013	1	f	管理者	2026-08-16 22:17:26.795377+09	013	C73IBYAXLCHZL6Q7NZOA6QA5WS3QFCTE	t	0	\N	20260808115851	\N	20260809011254	1	\N	\N
49	09	2001	ST-201	太田 恵子	09-st-201@example.jp	1	f	一般職員	\N	ST-201	BAJLRWKH2IU4TKYGRYXEUMAH5WCOU527	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
8	23	0021	23	愛知 恵子	aichi@example.jp	1	f	管理者	2026-07-17 02:18:00+09	23	NHY7LL65FMFTPP5E6E2MEDRUC6JM3JEC	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
2	01	0021	010	鈴木 太郎	010@010.010.010	1	f	管理者	2026-08-12 10:41:27.799578+09	010	733EDVY5LZSHZZYVH52VYSOYOXEIZKSI	t	0	\N	20260808115851	\N	20260809010935	1	\N	\N
89	01	0021	011	増田 大輔	011@011.011.011	1	f	管理者	2026-08-27 14:46:05.475013+09	011	6P6T4QI4ZQQ63PSD3JXB6NFCUQ2NTZIZ	t	0	\N	20260808150634	14	20260827072931	1	\N	\N
16	01	2041	ST-205	伊藤 和也	ito@mikasa.example.jp	1	f	管理者	2026-08-27 18:41:44.724855+09	ST-205	UYQ4UYWAP3JUPOKQ5XRMTZEDLA7RNQO2	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
1	00	0021	000	田中 一郎	001@001.001.001	1	f	管理者	2026-08-27 18:43:13.9044+09	000	WZOOCJSQ6IHWZC32MOSMFJ4C3XDAWPLV	t	0	\N	20260808115851	\N	20260809010912	1	\N	\N
22	20	2001	ST-211	井上 直樹	test@example.jp	1	f	一般職員	2026-08-27 18:35:19.353791+09	ST-211	5LVOCU72WXMYDMP4TD3RT4VXQATRSPCH	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
13	01	2001	014	松本 恵子	014@014.014.014	1	f	一般職員	2026-08-02 19:43:17.236438+09	014	EPJWY3LVRF27LWWL7E5UJ5I2BNUEK5NY	t	0	\N	20260808115851	\N	20260809011313	1	\N	\N
23	04	2001	ST-201	木村 陽子	04-st-201@example.jp	1	f	一般職員	\N	ST-201	MUBUJO2Y2JEBWBSCLJVBBG2CZCGTJAJV	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
24	04	2002	ST-202	林 大輔	04-st-202@example.jp	1	f	一般職員	\N	ST-202	RH3X42O65SQLLIEMJEN3XB5X5R3NKIXU	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
25	04	2003	ST-203	斎藤 由美	04-st-203@example.jp	1	f	一般職員	\N	ST-203	YVE66T6YG5ES6W5RCVST3WW2ZO47MXBZ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
26	24	2001	ST-201	清水 健一	24-st-201@example.jp	1	f	一般職員	\N	ST-201	LZXSBI5O4VQO7U4FGZEHEGSQQW2SVMRX	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
27	24	2002	ST-202	山口 恵美	24-st-202@example.jp	1	f	一般職員	\N	ST-202	HRGXB47DCDFFNIUVHBXS7NZKXTDLSKTD	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
28	24	2003	ST-203	森 拓也	24-st-203@example.jp	1	f	一般職員	\N	ST-203	CBW72IT76YXC5F6536HUR52RPP7VA2FW	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
29	08	2001	ST-201	池田 香織	08-st-201@example.jp	1	f	一般職員	\N	ST-201	DBPKILWZOPPGPTYP6ANVJIS5WXPFW7HL	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
30	08	2002	ST-202	橋本 誠	08-st-202@example.jp	1	f	一般職員	\N	ST-202	KM3EC33PCOTVKSHKLH6BOEOVIAIWP64L	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
31	08	2003	ST-203	阿部 明美	08-st-203@example.jp	1	f	一般職員	\N	ST-203	JFFYUC4BVEYXYD6L3TL5SJRCY445XO4U	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
32	36	2001	ST-201	石川 学	36-st-201@example.jp	1	f	一般職員	\N	ST-201	4LUITH3IK42CAJ7UYLM3IV4VKHKR2RSP	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
33	36	2002	ST-202	前田 智子	36-st-202@example.jp	1	f	一般職員	\N	ST-202	YH27FDSKPPJI4WKBYNH6EJEXUO6GREN5	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
34	36	2003	ST-203	藤田 淳	36-st-203@example.jp	1	f	一般職員	\N	ST-203	VNGE736GAHTXD2IHG2TWCFVFDO53LDYA	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
35	46	2001	ST-201	岡田 裕子	46-st-201@example.jp	1	f	一般職員	\N	ST-201	VQW75I66UD7JPYBOAZWP77PVXYJUQBSF	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
36	46	2002	ST-202	後藤 剛	46-st-202@example.jp	1	f	一般職員	\N	ST-202	TKOIUBWURZVPANHHAL3MB7GHARMEXOAJ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
37	46	2003	ST-203	長谷川 麻衣	46-st-203@example.jp	1	f	一般職員	\N	ST-203	GKZPSUUHF7AKLCF4RYMJ5IDYWDH6XGC4	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
38	14	2001	ST-201	村上 隆	14-st-201@example.jp	1	f	一般職員	\N	ST-201	ZNUOUHKVLSTYONXVZRINLVLMZBG4SM62	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
39	14	2002	ST-202	近藤 有紀	14-st-202@example.jp	1	f	一般職員	\N	ST-202	4TN5XQXP4UJSJMCZPD6KKOMWFUM755CR	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
40	14	2003	ST-203	石井 亮	14-st-203@example.jp	1	f	一般職員	\N	ST-203	JO2UJCBEVEL2ODDUFDJ24DWYQG3L2DXX	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
41	31	2001	ST-201	坂本 弘	31-st-201@example.jp	1	f	一般職員	\N	ST-201	FZSI2YIISZGNLMMU6LJNRNK5FE2WF6CO	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
44	02	2001	ST-201	遠藤 浩	02-st-201@example.jp	1	f	一般職員	\N	ST-201	4LSXUISQ3PX6VFDYLPLELC6DNERE6DZZ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
45	03	2001	ST-201	青木 健太	03-st-201@example.jp	1	f	一般職員	\N	ST-201	APURTBLAWXFRVSFEGD5IXMGJ2BIONLGW	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
46	05	2001	ST-201	藤井 洋平	05-st-201@example.jp	1	f	一般職員	\N	ST-201	ZXJO6C4VT32OYEX3Q5YRQ7KEJOFHRVGA	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
47	06	2001	ST-201	西村 陽介	06-st-201@example.jp	1	f	一般職員	\N	ST-201	CFG5RR4WYRMEMJSZZYMZCCPIT2254LRW	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
48	07	2001	ST-201	福田 花子	07-st-201@example.jp	1	f	一般職員	\N	ST-201	BSC2DFIHT4HLY2457NGJNAKJYWL23VFH	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
50	10	2001	ST-201	三浦 直子	10-st-201@example.jp	1	f	一般職員	\N	ST-201	AWGGWWHJ32UJ7UJEZBXPLDDXFU727V3P	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
51	11	2001	ST-201	藤原 美穂	11-st-201@example.jp	1	f	一般職員	\N	ST-201	GIJHEH2LM2RPKAQU3KTPZ7DDAGA77CYQ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
52	12	2001	ST-201	岡本 幸子	12-st-201@example.jp	1	f	一般職員	\N	ST-201	NQ67NUKAPOLWM2LYARNCVEOSKO4F6CL6	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
53	13	2001	ST-201	松田 一郎	13-st-201@example.jp	1	f	一般職員	\N	ST-201	DMCW26URINJCSLMY2PFQF33EDM64R52Y	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
54	15	2001	ST-201	中野 太郎	15-st-201@example.jp	1	f	一般職員	\N	ST-201	CNN33QLJS6XWYFAY4OMK4OKRXQ77U3EZ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
55	16	2001	ST-201	原田 次郎	16-st-201@example.jp	1	f	一般職員	\N	ST-201	T4RG2F2KJT7XSMG5GSB6AA4DCVDLHGD7	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
56	17	2001	ST-201	小川 三郎	17-st-201@example.jp	1	f	一般職員	\N	ST-201	2P3BHIA52DSTMFKO77BHU3H5LKUYLTBZ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
57	18	2001	ST-201	竹内 修	18-st-201@example.jp	1	f	一般職員	\N	ST-201	M5P5MXOJANEI64YTTCMRGJOCTYZV5XSU	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
58	19	2001	ST-201	金子 誠	19-st-201@example.jp	1	f	一般職員	\N	ST-201	EQW57HZT6QL6PCVVWFC5PZKBEHKQ2KT6	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
59	21	2001	ST-201	和田 明	21-st-201@example.jp	1	f	一般職員	\N	ST-201	PKIXX5U42ERTYFP6VL6SK47M7NSB7VJE	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
60	22	2001	ST-201	中山 学	22-st-201@example.jp	1	f	一般職員	\N	ST-201	VWDTME6KOCW2RY6R5HZQ2NGPJA6BUPHA	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
61	23	2001	ST-201	石田 淳	23-st-201@example.jp	1	f	一般職員	\N	ST-201	BSVVHBP4FYIUKUDJCUEU43TNIWI2FPVN	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
62	25	2001	ST-201	上田 剛	25-st-201@example.jp	1	f	一般職員	\N	ST-201	OP43Q24Y4MVRSEY3KZ22OVATRQ5OF5U3	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
63	26	2001	ST-201	森田 隆	26-st-201@example.jp	1	f	一般職員	\N	ST-201	4546KZE6ZRMCMHXWQUD4BOFKOV3WLGSH	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
64	27	2001	ST-201	柴田 亮	27-st-201@example.jp	1	f	一般職員	\N	ST-201	HNIFK7LWB5N4D7YTMIACWLKTQN2GNYFX	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
65	28	2001	ST-201	酒井 弘	28-st-201@example.jp	1	f	一般職員	\N	ST-201	H2R7MSEHQ6AZC762ZIVA6SLRNZNBYS3M	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
66	29	2001	ST-201	工藤 浩	29-st-201@example.jp	1	f	一般職員	\N	ST-201	RULFZMVUQXGETINPAK5OSIAKSE5XESWE	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
67	30	2001	ST-201	横山 健一	30-st-201@example.jp	1	f	一般職員	\N	ST-201	L5WSJT723OIPNVAF4NYIANXOAF5SKO7B	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
68	32	2001	ST-201	宮崎 洋平	32-st-201@example.jp	1	f	一般職員	\N	ST-201	34FHTGQVVHHCTWXF2O3J7RNTQ4RL52C6	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
69	33	2001	ST-201	内田 陽介	33-st-201@example.jp	1	f	一般職員	\N	ST-201	CF2LMU5GNLX2Z6PR2QBQ3D4QK4TAR3IK	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
70	34	2001	ST-201	高田 花子	34-st-201@example.jp	1	f	一般職員	\N	ST-201	JPO6O53BTG3A35OKCEVYQUA274I32PIP	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
71	35	2001	ST-201	安藤 恵子	35-st-201@example.jp	1	f	一般職員	\N	ST-201	PCYAH5C2C65FRQF4UWSCHRPORJXBQ75N	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
72	37	2001	ST-201	谷口 由美	37-st-201@example.jp	1	f	一般職員	\N	ST-201	3WJIVNQ5IZ3BZQRMSK3LNDMGF66HVF3G	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
73	38	2001	ST-201	大野 久美子	38-st-201@example.jp	1	f	一般職員	\N	ST-201	WU3O3DGRAK7ZI6D7B6MBGQC5TXMQMMQV	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
74	39	2001	ST-201	丸山 美咲	39-st-201@example.jp	1	f	一般職員	\N	ST-201	6QCECZFYBF4KJGZ2CVWYCYFYWGIAY65S	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
75	40	2001	ST-201	今井 陽子	40-st-201@example.jp	1	f	一般職員	\N	ST-201	55UZGMXSDJG3RB5VHMZKITSWMJAF5D6B	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
76	41	2001	ST-201	高橋 恵美	41-st-201@example.jp	1	f	一般職員	\N	ST-201	J6LZOHBE7NQ75B6WAZND32FSLPD4GNK2	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
77	42	2001	ST-201	河野 直子	42-st-201@example.jp	1	f	一般職員	\N	ST-201	UABXUDHQJCJP6NAPBV6VTBZMZN352DWQ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
78	43	2001	ST-201	藤本 香織	43-st-201@example.jp	1	f	一般職員	\N	ST-201	W24QTKTHFSQZ24BUYGA2VXXWJXE74PA3	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
79	44	2001	ST-201	村田 麻衣	44-st-201@example.jp	1	f	一般職員	\N	ST-201	ZISWM5ORFGA4KVRCGKLOJQN2ZDRDITMZ	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
80	45	2001	ST-201	武田 有紀	45-st-201@example.jp	1	f	一般職員	\N	ST-201	RP7FYS4C2BUDJCFCRLOH2AFGBRFZK57P	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
81	47	2001	ST-201	上野 智子	47-st-201@example.jp	1	f	一般職員	\N	ST-201	K6MYHMLXE3UDU7PHFE766ZGQIF3HTQ2L	t	0	\N	20260808115851	\N	20260808115851	\N	\N	\N
87	01	2020	plainid1	杉山 健太	plainid1@example.com	1	f	一般職員	\N	Passw0rd!	KCGQTMLKO4EXWOFFLVBRYXORLBJNMJFB	t	0	\N	20260808130649	1	20260808154634	2	\N	\N
91	00	0021	001	平野 拓也	001@001.001.001	1	f	一般職員	2026-08-09 00:47:29.471615+09	001	HTXCJKB2R4VU35F3AER37IICQWGEFOHG	t	0	\N	20260808155122	1	20260827122330	1	\N	\N
90	01	0021	012	小島 直樹	012@012.012.012	1	f	県連（商工会権限）	2026-08-27 13:18:18.483039+09	012	FUMU2ZKSMG6KDEDLJFIU63MKOCMLPWYJ	t	0	\N	20260808150749	89	20260809011000	1	\N	\N
\.


--
-- Data for Name: mst_user_account_qualification; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_user_account_qualification (user_account_id, qualification_id) FROM stdin;
\.


--
-- Data for Name: mst_visit_result; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mst_visit_result (visit_result_id, fiscal_year_id, visit_result_code, label, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	3	v1	支援継続	1	20260813065853	\N	20260813065853	\N	\N	\N
2	3	v2	支援完了	2	20260813065853	\N	20260813065853	\N	\N	\N
3	3	v3	不在・再訪問要	3	20260813065853	\N	20260813065853	\N	\N	\N
4	3	v4	その他	4	20260813065853	\N	20260813065853	\N	\N	\N
\.


--
-- Data for Name: trn_ai_usage_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_ai_usage_log (ai_usage_log_id, used_at, user_account_id, feature, input_content, output_content) FROM stdin;
4	2026-08-09 12:28:40.517007+09	90	ai_proposal.generate	業種: 卸売業、小売業 / 支援テーマ: 賃上げ・最低賃金引上げ / 相談概要: 最低賃金引き上げ対応で人件費が増加。売上は横ばいで財源確保に悩んでいる。価格転嫁も検討中。	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。\n\n価格転嫁支援・交渉支援\nコスト増加分を価格に転嫁する交渉を、専門家と一緒に進めてみませんか。これなら、価格設定の見直しと顧客への説明の仕方が整理でき、無理のない形で収益を確保できます。
5	2026-08-22 23:18:49.530983+09	1	ai_proposal.generate	業種: 卸売業、小売業 / 支援テーマ: 賃上げ・最低賃金引上げ / 相談概要: 最低賃金引き上げ対応で人件費が増加。売上は横ばいで財源確保に悩んでいる。価格転嫁も検討中。	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。\n\n価格転嫁支援・交渉支援\nコスト増加分を価格に転嫁する交渉を、専門家と一緒に進めてみませんか。これなら、価格設定の見直しと顧客への説明の仕方が整理でき、無理のない形で収益を確保できます。
6	2026-08-22 23:19:07.266461+09	90	ai_proposal.generate	業種: 卸売業、小売業 / 支援テーマ: 賃上げ・最低賃金引上げ / 相談概要: 最低賃金引き上げ対応で人件費が増加。売上は横ばいで財源確保に悩んでいる。価格転嫁も検討中。	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。\n\n価格転嫁支援・交渉支援\nコスト増加分を価格に転嫁する交渉を、専門家と一緒に進めてみませんか。これなら、価格設定の見直しと顧客への説明の仕方が整理でき、無理のない形で収益を確保できます。
7	2026-08-26 21:38:46.94671+09	22	ai_proposal.generate	業種:  / 支援テーマ: 賃上げ・最低賃金引上げ / 相談概要: 最低賃金引き上げ対応で人件費が増加している。	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。申請書類の作成から生産性向上計画の策定まで、商工会の窓口で一緒に整理しながら進められるため、初めての申請でも安心して取り組めます。\n\n価格転嫁支援・交渉支援\n原材料費や人件費の上昇分を算出し、その根拠資料をそろえたうえで取引先へ値上げを打診してみませんか。コスト上昇の内訳を数字で示しながら交渉することで、価格改定について取引先の理解を得やすくなり、無理のない形で利益率を回復できます。交渉の切り出し方や想定される反論への返し方まで専門家が具体的にアドバイスするため、値上げ交渉に不慣れな場合でも落ち着いて対応できます。
8	2026-08-26 21:38:48.747103+09	22	ai_proposal.knowledge_search	インボイス	
9	2026-08-26 21:39:19.889936+09	22	ai_proposal.knowledge_search	最低賃金	都道府県別 最低賃金改定額（令和8年度）
10	2026-08-26 21:49:00.221665+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
11	2026-08-26 22:48:30.816838+09	90	ai_proposal.generate	業種:  / 支援テーマ:  / 相談概要: 補助金	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。申請書類の作成から生産性向上計画の策定まで、商工会の窓口で一緒に整理しながら進められるため、初めての申請でも安心して取り組めます。\n\n価格転嫁支援・交渉支援\n原材料費や人件費の上昇分を算出し、その根拠資料をそろえたうえで取引先へ値上げを打診してみませんか。コスト上昇の内訳を数字で示しながら交渉することで、価格改定について取引先の理解を得やすくなり、無理のない形で利益率を回復できます。交渉の切り出し方や想定される反論への返し方まで専門家が具体的にアドバイスするため、値上げ交渉に不慣れな場合でも落ち着いて対応できます。
12	2026-08-26 22:49:56.671399+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
13	2026-08-26 22:51:15.358323+09	22	ai_proposal.knowledge_search	インボイス	
14	2026-08-26 22:51:55.814557+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
15	2026-08-27 07:22:15.478648+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
16	2026-08-27 07:23:27.67682+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
17	2026-08-27 07:23:29.233485+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
18	2026-08-27 11:54:15.143009+09	22	ai_proposal.generate	業種:  / 支援テーマ: 賃上げ・最低賃金引上げ / 相談概要: 最低賃金引き上げへの対応に困っている	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。申請書類の作成から生産性向上計画の策定まで、商工会の窓口で一緒に整理しながら進められるため、初めての申請でも安心して取り組めます。\n\n価格転嫁支援・交渉支援\n原材料費や人件費の上昇分を算出し、その根拠資料をそろえたうえで取引先へ値上げを打診してみませんか。コスト上昇の内訳を数字で示しながら交渉することで、価格改定について取引先の理解を得やすくなり、無理のない形で利益率を回復できます。交渉の切り出し方や想定される反論への返し方まで専門家が具体的にアドバイスするため、値上げ交渉に不慣れな場合でも落ち着いて対応できます。
19	2026-08-27 11:54:16.245873+09	22	ai_proposal.knowledge_search	補助	省力化投資補助金 対象設備の判定基準、商工会法における組織運営の基本
20	2026-08-27 11:54:42.765571+09	22	ai_proposal.generate	業種:  / 支援テーマ: 賃上げ・最低賃金引上げ / 相談概要: 最低賃金引き上げへの対応に困っている	業務改善助成金の活用\n業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。申請書類の作成から生産性向上計画の策定まで、商工会の窓口で一緒に整理しながら進められるため、初めての申請でも安心して取り組めます。\n\n価格転嫁支援・交渉支援\n原材料費や人件費の上昇分を算出し、その根拠資料をそろえたうえで取引先へ値上げを打診してみませんか。コスト上昇の内訳を数字で示しながら交渉することで、価格改定について取引先の理解を得やすくなり、無理のない形で利益率を回復できます。交渉の切り出し方や想定される反論への返し方まで専門家が具体的にアドバイスするため、値上げ交渉に不慣れな場合でも落ち着いて対応できます。
21	2026-08-27 11:54:43.851948+09	22	ai_proposal.knowledge_search	補助	省力化投資補助金 対象設備の判定基準、商工会法における組織運営の基本
22	2026-08-27 12:34:18.884486+09	1	ai_proposal.knowledge_search	zzznomatchzzz	
23	2026-08-27 13:14:03.719304+09	89	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
24	2026-08-27 13:14:31.604295+09	89	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
25	2026-08-27 13:15:31.877194+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
26	2026-08-27 14:28:49.092944+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
27	2026-08-27 14:31:02.717262+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
28	2026-08-27 14:31:44.523049+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
29	2026-08-27 14:32:19.757026+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
30	2026-08-27 14:32:33.506041+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
31	2026-08-27 14:33:07.054542+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
32	2026-08-27 14:33:37.990221+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
33	2026-08-27 14:33:40.120848+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
34	2026-08-27 14:35:03.731344+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
35	2026-08-27 14:35:09.127198+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
36	2026-08-27 14:35:14.364207+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
37	2026-08-27 14:35:32.396572+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
38	2026-08-27 14:37:13.775968+09	22	ai_proposal.knowledge_search	賃上げ	賃上げ促進税制の適用要件まとめ
39	2026-08-27 14:37:46.130603+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
40	2026-08-27 14:38:57.449594+09	90	ai_proposal.knowledge_search		賃上げ促進税制の適用要件まとめ、省力化投資補助金 対象設備の判定基準、事業承継税制の特例措置一覧、都道府県別 最低賃金改定額（令和8年度）、専門家派遣事業 申込フロー、商工会法における組織運営の基本
\.


--
-- Data for Name: trn_change_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_change_history (change_history_id, changed_at, changed_by, feature, table_name, record_id, action, detail, before_value, after_value) FROM stdin;
1	2026-08-08 12:17:10.491713+09	16	manual_input.create_report	trn_report	115	作成	報告書登録: report_code=RPT-0105, status=下書き	\N	{"status": "下書き", "summary": "", "form_code": null, "report_date": null}
2	2026-08-08 12:17:10.550092+09	16	manual_input.delete_report	trn_report	115	削除	報告書削除（論理削除）: report_code=RPT-0105	{"status": "下書き", "content": "", "summary": "", "theme_id": null, "time_end": "", "form_code": null, "report_id": 115, "created_at": "2026-08-08 12:17:10.491713+09:00", "created_by": 16, "deleted_at": null, "deleted_by": null, "time_start": "", "updated_at": "2026-08-08 12:17:10.491713+09:00", "updated_by": 16, "report_code": "RPT-0105", "report_date": null, "shokokai_cd": "2041", "business_name": "", "industry_code": null, "registered_at": "2026-08-08", "fiscal_year_id": 3, "industry_label": null, "staff_sub_name": null, "business_person": "", "form_full_label": null, "prefecture_code": "01", "staff_main_name": "", "voice_transcript": null, "primary_theme_code": null}	\N
3	2026-08-08 12:17:48.067311+09	1	accounts.update	mst_user_account	4	更新	\N	{"email": "iwate@example.jp", "status": 0, "user_id": "03", "shokuin_kj": "岩手 次郎", "shokokai_cd": "0021", "prefecture_code": "03", "permission_level": "一般職員"}	{"email": "iwate@example.jp", "status": 0, "user_id": "03", "shokuin_kj": "岩手 次郎", "shokokai_cd": "0021", "prefecture_code": "03", "permission_level": "一般職員"}
4	2026-08-08 12:17:48.129653+09	1	knowledge.create_entry	trn_knowledge_entry	13	作成	知識データ登録: knowledge_code=KN-012, status=下書き	\N	{"title": "audit-test-entry", "status": "下書き", "knowledge_document_id": null}
5	2026-08-08 12:17:48.159818+09	1	knowledge.delete_entry	trn_knowledge_entry	13	削除	知識データ削除: knowledge_code=KN-012	{"title": "audit-test-entry", "status": "下書き", "content": "test content", "created_at": "2026-08-08 12:17:48.129653+09:00", "created_by": 1, "deleted_at": null, "deleted_by": null, "updated_at": "2026-08-08 12:17:48.129653+09:00", "updated_by": 1, "updated_date": "2026-08-08", "document_title": null, "knowledge_code": "KN-012", "prefecture_code": null, "prefecture_name": null, "document_category": null, "knowledge_entry_id": 13, "knowledge_document_id": null}	\N
6	2026-08-08 12:18:50.218146+09	1	accounts.create	mst_user_account	86	作成	アカウント作成: user_id=AIaudittest1, permission_level=一般職員	\N	{"email": "audittest1@example.com", "status": 1, "user_id": "AIaudittest1", "shokuin_kj": "テスト太郎", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}
7	2026-08-08 12:18:50.24811+09	1	accounts.delete	mst_user_account	86	削除	アカウント削除: user_id=AIaudittest1	{"email": "audittest1@example.com", "status": 1, "user_id": "AIaudittest1", "shokuin_kj": "テスト太郎", "core_linked": false, "shokokai_cd": "2001", "last_login_at": null, "shokokai_name": "石狩北商工会", "prefecture_code": "01", "prefecture_name": "北海道", "user_account_id": 86, "permission_level": "一般職員"}	\N
8	2026-08-08 12:51:16.852008+09	14	accounts.update	mst_user_account	14	更新	\N	{"email": "sato@shiriuchi.example.jp", "status": 1, "user_id": "ST-203", "shokuin_kj": "佐藤 三郎", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "sato@shiriuchi.example.jp", "status": 1, "user_id": "ST-203", "shokuin_kj": "佐藤 三郎", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}
9	2026-08-08 12:51:29.3556+09	1	knowledge.create_entry	trn_knowledge_entry	14	作成	知識データ登録: knowledge_code=KN-012, status=下書き	\N	{"title": "merge-test", "status": "下書き", "knowledge_document_id": null}
10	2026-08-08 12:51:42.686953+09	14	accounts.update	mst_user_account	14	更新	\N	{"email": "sato@shiriuchi.example.jp", "status": 1, "user_id": "ST-203", "shokuin_kj": "佐藤 三郎", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "sato@shiriuchi.example.jp", "status": 1, "user_id": "ST-203", "shokuin_kj": "佐藤 三郎", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}
11	2026-08-08 13:06:49.823286+09	1	accounts.create	mst_user_account	87	作成	アカウント作成: user_id=plainid1, permission_level=一般職員	\N	{"email": "plainid1@example.com", "status": 1, "user_id": "plainid1", "shokuin_kj": "テスト太郎2", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}
12	2026-08-08 15:05:38.10073+09	1	manual_input.create_report	trn_report	116	作成	報告書登録: report_code=RPT-0106, status=下書き	\N	{"status": "下書き", "summary": "", "form_code": null, "report_date": null}
13	2026-08-08 15:05:48.282781+09	1	manual_input.create_report	trn_report	117	作成	報告書登録: report_code=RPT-0107, status=下書き	\N	{"status": "下書き", "summary": "", "form_code": null, "report_date": null}
14	2026-08-08 15:06:34.146858+09	14	accounts.create	mst_user_account	89	作成	アカウント作成: user_id=011, permission_level=マスタ管理者	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "職員名", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "マスタ管理者"}
15	2026-08-08 15:07:28.068493+09	89	accounts.update	mst_user_account	89	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "職員名", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "マスタ管理者"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "マスタ管理者", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "マスタ管理者"}
16	2026-08-08 15:07:49.605399+09	89	accounts.create	mst_user_account	90	作成	アカウント作成: user_id=012, permission_level=一般職員	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "一般職員", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}
17	2026-08-08 15:26:39.040471+09	2	accounts.update	mst_user_account	14	更新	\N	{"email": "sato@shiriuchi.example.jp", "status": 1, "user_id": "ST-203", "shokuin_kj": "佐藤 三郎", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "sato@shiriuchi.example.jp", "status": 1, "user_id": "ST-203", "shokuin_kj": "佐藤 三郎", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}
18	2026-08-08 15:26:46.131387+09	2	accounts.update	mst_user_account	90	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "一般職員", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "一般職員", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}
61	2026-08-09 01:09:39.067612+09	\N	manual_input.create_report	trn_report	137	作成	報告書登録: report_code=RPT-0020, status=登録済み	\N	{"status": "登録済み", "summary": "輸出先多角化の相談", "form_code": "G-7", "report_date": "2025-10-13"}
19	2026-08-08 15:46:34.331492+09	2	accounts.update	mst_user_account	87	更新	\N	{"email": "plainid1@example.com", "status": 1, "user_id": "plainid1", "shokuin_kj": "テスト太郎2", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "plainid1@example.com", "status": 1, "user_id": "plainid1", "shokuin_kj": "テスト太郎2", "shokokai_cd": "2020", "prefecture_code": "01", "permission_level": "一般職員"}
20	2026-08-08 15:49:57.845532+09	1	accounts.update	mst_user_account	1	更新	\N	{"email": "yamada@example.jp", "status": 1, "user_id": "00", "shokuin_kj": "山田 太郎", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}	{"email": "yamada@example.jp", "status": 1, "user_id": "00", "shokuin_kj": "システム管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}
21	2026-08-08 15:50:08.649087+09	1	accounts.update	mst_user_account	1	更新	\N	{"email": "yamada@example.jp", "status": 1, "user_id": "00", "shokuin_kj": "システム管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}	{"email": "yamada@example.jp", "status": 1, "user_id": "00", "shokuin_kj": "全国連システム管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}
22	2026-08-08 15:51:22.511513+09	1	accounts.create	mst_user_account	91	作成	アカウント作成: user_id=001, permission_level=一般職員	\N	{"email": "111@1111.1111", "status": 1, "user_id": "001", "shokuin_kj": "全国連一般職員", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}
23	2026-08-08 15:51:31.820351+09	1	accounts.update	mst_user_account	1	更新	\N	{"email": "yamada@example.jp", "status": 1, "user_id": "00", "shokuin_kj": "全国連システム管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}	{"email": "yamada@example.jp", "status": 1, "user_id": "000", "shokuin_kj": "全国連システム管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}
24	2026-08-08 15:52:49.426767+09	1	accounts.update	mst_user_account	1	更新	\N	{"email": "yamada@example.jp", "status": 1, "user_id": "000", "shokuin_kj": "全国連システム管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}	{"email": "yamada@example.jp", "status": 1, "user_id": "000", "shokuin_kj": "全国連管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "システム管理者"}
25	2026-08-08 17:19:44.478234+09	1	accounts.update	mst_user_account	2	更新	\N	{"email": "hokkaido@example.com", "status": 1, "user_id": "01", "shokuin_kj": "テスト北海道職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "hokkaido@example.com", "status": 1, "user_id": "010", "shokuin_kj": "テスト北海道職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}
26	2026-08-08 17:21:30.812989+09	1	accounts.update	mst_user_account	89	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "マスタ管理者", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "マスタ管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}
27	2026-08-08 17:21:40.338691+09	1	accounts.update	mst_user_account	89	更新	permission_level: 管理者 → 一般職員	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "マスタ管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "マスタ管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}
28	2026-08-08 17:22:30.44261+09	1	accounts.update	mst_user_account	90	更新	permission_level: 一般職員 → 県連（商工会権限）	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "一般職員", "shokokai_cd": "2010", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "北海道商工会県g年", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "県連（商工会権限）"}
29	2026-08-09 00:32:49.589767+09	1	knowledge.update_document	mst_knowledge_document	1	更新	\N	{"title": "商工会法 逐条解説（令和6年版）", "format": "PDF", "category": "法令・制度"}	{"title": "商工会法 逐条解説（令和6年版）", "format": "PDF", "category": "法令・制度"}
30	2026-08-09 00:34:57.739862+09	1	knowledge.resync	trn_vector_collection	ALL	更新	全6コレクションを一括再同期しました	\N	\N
31	2026-08-09 00:36:17.843329+09	1	knowledge.create_document	mst_knowledge_document	12	作成	文書登録: document_code=doc-010, title=テストアップロード文書	\N	{"title": "テストアップロード文書", "format": "PDF", "category": "税制", "prefecture_code": null}
32	2026-08-09 00:37:34.058078+09	1	knowledge.update_document	mst_knowledge_document	1	更新	\N	{"title": "商工会法 逐条解説（令和6年版）", "format": "PDF", "category": "法令・制度"}	{"title": "商工会法 逐条解説（令和6年版）", "format": "PDF", "category": "法令・制度"}
33	2026-08-09 00:37:50.912261+09	1	knowledge.add_document_version	mst_knowledge_document_version	2:3	作成	新しい版を登録・有効化: version=3	\N	\N
34	2026-08-09 00:38:06.958432+09	1	knowledge.add_document_version	mst_knowledge_document_version	2:4	作成	新しい版を登録・有効化: version=4	\N	\N
35	2026-08-09 00:40:22.886903+09	1	accounts.update	mst_user_account	90	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "北海道商工会県g年", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "県連（商工会権限）"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "北海道商工会権限", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "県連（商工会権限）"}
36	2026-08-09 00:40:52.094526+09	1	accounts.update	mst_user_account	89	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "マスタ管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "北海道マスタ管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}
62	2026-08-09 01:09:39.069471+09	\N	manual_input.create_report	trn_report	138	作成	報告書登録: report_code=RPT-0021, status=登録済み	\N	{"status": "登録済み", "summary": "事業再構築の相談", "form_code": "G-4", "report_date": "2026-04-17"}
37	2026-08-09 00:41:08.592796+09	1	accounts.update	mst_user_account	2	更新	\N	{"email": "hokkaido@example.com", "status": 1, "user_id": "010", "shokuin_kj": "テスト北海道職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "hokkaido@example.com", "status": 1, "user_id": "010", "shokuin_kj": "北海道管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}
38	2026-08-09 00:41:31.761332+09	1	accounts.update	mst_user_account	89	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "北海道マスタ管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "北海道\\t一般職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}
39	2026-08-09 01:09:12.896682+09	1	accounts.update	mst_user_account	1	更新	\N	{"email": "yamada@example.jp", "status": 1, "user_id": "000", "shokuin_kj": "全国連管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "管理者"}	{"email": "001@001.001.001", "status": 1, "user_id": "000", "shokuin_kj": "全国連管理者", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "管理者"}
40	2026-08-09 01:09:24.415745+09	1	accounts.update	mst_user_account	91	更新	\N	{"email": "111@1111.1111", "status": 1, "user_id": "001", "shokuin_kj": "全国連一般職員", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}	{"email": "001@001.001.001", "status": 1, "user_id": "001", "shokuin_kj": "全国連一般職員", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}
41	2026-08-09 01:09:35.450612+09	1	accounts.update	mst_user_account	2	更新	\N	{"email": "hokkaido@example.com", "status": 1, "user_id": "010", "shokuin_kj": "北海道管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "010@010.010.010", "status": 1, "user_id": "010", "shokuin_kj": "北海道管理者", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}
42	2026-08-09 01:09:38.999218+09	\N	manual_input.create_report	trn_report	118	作成	報告書登録: report_code=RPT-0001, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "G-2", "report_date": "2026-05-12"}
43	2026-08-09 01:09:39.030846+09	\N	manual_input.create_report	trn_report	119	作成	報告書登録: report_code=RPT-0002, status=登録済み	\N	{"status": "登録済み", "summary": "2割特例適用の相談", "form_code": "F", "report_date": "2026-06-13"}
44	2026-08-09 01:09:39.034046+09	\N	manual_input.create_report	trn_report	120	作成	報告書登録: report_code=RPT-0003, status=登録済み	\N	{"status": "登録済み", "summary": "事業再構築の相談", "form_code": "G-6", "report_date": "2025-11-09"}
45	2026-08-09 01:09:39.036458+09	\N	manual_input.create_report	trn_report	121	作成	報告書登録: report_code=RPT-0004, status=登録済み	\N	{"status": "登録済み", "summary": "業務フロー見直し相談", "form_code": "G-3", "report_date": "2025-10-10"}
46	2026-08-09 01:09:39.038556+09	\N	manual_input.create_report	trn_report	122	作成	報告書登録: report_code=RPT-0005, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁の進め方相談", "form_code": "G-4", "report_date": "2026-04-27"}
47	2026-08-09 01:09:39.040844+09	\N	manual_input.create_report	trn_report	123	作成	報告書登録: report_code=RPT-0006, status=登録済み	\N	{"status": "登録済み", "summary": "クラウド会計導入相談", "form_code": "G-4", "report_date": "2026-06-10"}
48	2026-08-09 01:09:39.043324+09	\N	manual_input.create_report	trn_report	124	作成	報告書登録: report_code=RPT-0007, status=登録済み	\N	{"status": "登録済み", "summary": "経理体制整備の相談", "form_code": "G-8", "report_date": "2026-03-17"}
49	2026-08-09 01:09:39.044625+09	\N	manual_input.create_report	trn_report	125	作成	報告書登録: report_code=RPT-0008, status=登録済み	\N	{"status": "登録済み", "summary": "補助金申請書類整理の相談", "form_code": "G-7", "report_date": "2026-04-16"}
50	2026-08-09 01:09:39.046108+09	\N	manual_input.create_report	trn_report	126	作成	報告書登録: report_code=RPT-0009, status=登録済み	\N	{"status": "登録済み", "summary": "省力化補助金の活用相談", "form_code": "G-5", "report_date": "2026-01-18"}
51	2026-08-09 01:09:39.047492+09	\N	manual_input.create_report	trn_report	127	作成	報告書登録: report_code=RPT-0010, status=登録済み	\N	{"status": "登録済み", "summary": "多能工化の相談", "form_code": "G-7", "report_date": "2026-04-25"}
52	2026-08-09 01:09:39.051655+09	\N	manual_input.create_report	trn_report	128	作成	報告書登録: report_code=RPT-0011, status=登録済み	\N	{"status": "登録済み", "summary": "事業再構築の相談", "form_code": "G-2", "report_date": "2026-07-01"}
53	2026-08-09 01:09:39.053623+09	\N	manual_input.create_report	trn_report	129	作成	報告書登録: report_code=RPT-0012, status=登録済み	\N	{"status": "登録済み", "summary": "2割特例適用の相談", "form_code": "G-5", "report_date": "2026-02-03"}
54	2026-08-09 01:09:39.055072+09	\N	manual_input.create_report	trn_report	130	作成	報告書登録: report_code=RPT-0013, status=登録済み	\N	{"status": "登録済み", "summary": "省エネ設備導入相談", "form_code": "G-3", "report_date": "2025-09-29"}
55	2026-08-09 01:09:39.056687+09	\N	manual_input.create_report	trn_report	131	作成	報告書登録: report_code=RPT-0014, status=登録済み	\N	{"status": "登録済み", "summary": "多能工化の相談", "form_code": "G-6", "report_date": "2026-03-08"}
56	2026-08-09 01:09:39.059164+09	\N	manual_input.create_report	trn_report	132	作成	報告書登録: report_code=RPT-0015, status=登録済み	\N	{"status": "登録済み", "summary": "ECサイト構築相談", "form_code": "G-2", "report_date": "2025-12-06"}
57	2026-08-09 01:09:39.060484+09	\N	manual_input.create_report	trn_report	133	作成	報告書登録: report_code=RPT-0016, status=登録済み	\N	{"status": "登録済み", "summary": "月次報告書作成の相談", "form_code": "F", "report_date": "2026-03-08"}
58	2026-08-09 01:09:39.061818+09	\N	manual_input.create_report	trn_report	134	作成	報告書登録: report_code=RPT-0017, status=登録済み	\N	{"status": "登録済み", "summary": "月次報告書作成の相談", "form_code": "G-8", "report_date": "2026-04-15"}
59	2026-08-09 01:09:39.063742+09	\N	manual_input.create_report	trn_report	135	作成	報告書登録: report_code=RPT-0018, status=登録済み	\N	{"status": "登録済み", "summary": "経理体制整備の相談", "form_code": "F", "report_date": "2026-01-15"}
60	2026-08-09 01:09:39.065779+09	\N	manual_input.create_report	trn_report	136	作成	報告書登録: report_code=RPT-0019, status=登録済み	\N	{"status": "登録済み", "summary": "コロナ融資返済相談", "form_code": "G-6", "report_date": "2026-04-30"}
63	2026-08-09 01:09:39.071445+09	\N	manual_input.create_report	trn_report	139	作成	報告書登録: report_code=RPT-0022, status=登録済み	\N	{"status": "登録済み", "summary": "最低賃金引上げへの対応相談", "form_code": "G-7", "report_date": "2026-06-05"}
64	2026-08-09 01:09:39.073422+09	\N	manual_input.create_report	trn_report	140	作成	報告書登録: report_code=RPT-0023, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁交渉の相談", "form_code": "G-6", "report_date": "2026-05-26"}
65	2026-08-09 01:09:39.075025+09	\N	manual_input.create_report	trn_report	141	作成	報告書登録: report_code=RPT-0024, status=登録済み	\N	{"status": "登録済み", "summary": "輸出先多角化の相談", "form_code": "G-4", "report_date": "2025-12-11"}
66	2026-08-09 01:09:39.076254+09	\N	manual_input.create_report	trn_report	142	作成	報告書登録: report_code=RPT-0025, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "F", "report_date": "2026-03-13"}
67	2026-08-09 01:09:39.078242+09	\N	manual_input.create_report	trn_report	143	作成	報告書登録: report_code=RPT-0026, status=登録済み	\N	{"status": "登録済み", "summary": "補助金申請書類整理の相談", "form_code": "G-5", "report_date": "2026-05-30"}
68	2026-08-09 01:09:39.080364+09	\N	manual_input.create_report	trn_report	144	作成	報告書登録: report_code=RPT-0027, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁の進め方相談", "form_code": "G-7", "report_date": "2026-04-01"}
69	2026-08-09 01:09:39.084952+09	\N	manual_input.create_report	trn_report	145	作成	報告書登録: report_code=RPT-0028, status=登録済み	\N	{"status": "登録済み", "summary": "月次報告書作成の相談", "form_code": "G-6", "report_date": "2026-07-13"}
70	2026-08-09 01:09:39.087239+09	\N	manual_input.create_report	trn_report	146	作成	報告書登録: report_code=RPT-0029, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "F", "report_date": "2026-02-24"}
71	2026-08-09 01:09:39.08907+09	\N	manual_input.create_report	trn_report	147	作成	報告書登録: report_code=RPT-0030, status=登録済み	\N	{"status": "登録済み", "summary": "最低賃金引上げへの対応相談", "form_code": "G-3", "report_date": "2026-07-28"}
72	2026-08-09 01:09:39.091358+09	\N	manual_input.create_report	trn_report	148	作成	報告書登録: report_code=RPT-0031, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "G-8", "report_date": "2025-12-14"}
73	2026-08-09 01:09:39.09326+09	\N	manual_input.create_report	trn_report	149	作成	報告書登録: report_code=RPT-0032, status=登録済み	\N	{"status": "登録済み", "summary": "月次報告書作成の相談", "form_code": "G-5", "report_date": "2026-05-09"}
74	2026-08-09 01:09:39.094727+09	\N	manual_input.create_report	trn_report	150	作成	報告書登録: report_code=RPT-0033, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁の進め方相談", "form_code": "G-3", "report_date": "2025-10-11"}
75	2026-08-09 01:09:39.096767+09	\N	manual_input.create_report	trn_report	151	作成	報告書登録: report_code=RPT-0034, status=登録済み	\N	{"status": "登録済み", "summary": "ECサイト構築相談", "form_code": "G-7", "report_date": "2026-05-23"}
76	2026-08-09 01:09:39.098294+09	\N	manual_input.create_report	trn_report	152	作成	報告書登録: report_code=RPT-0035, status=登録済み	\N	{"status": "登録済み", "summary": "新商品開発の相談", "form_code": "G-5", "report_date": "2026-04-09"}
77	2026-08-09 01:09:39.100539+09	\N	manual_input.create_report	trn_report	153	作成	報告書登録: report_code=RPT-0036, status=登録済み	\N	{"status": "登録済み", "summary": "省力化補助金の活用相談", "form_code": "G-8", "report_date": "2025-12-10"}
78	2026-08-09 01:09:39.102084+09	\N	manual_input.create_report	trn_report	154	作成	報告書登録: report_code=RPT-0037, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "G-7", "report_date": "2026-06-13"}
79	2026-08-09 01:09:39.104016+09	\N	manual_input.create_report	trn_report	155	作成	報告書登録: report_code=RPT-0038, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "G-2", "report_date": "2026-05-24"}
80	2026-08-09 01:09:39.106274+09	\N	manual_input.create_report	trn_report	156	作成	報告書登録: report_code=RPT-0039, status=登録済み	\N	{"status": "登録済み", "summary": "実績報告準備の相談", "form_code": "G-5", "report_date": "2026-06-09"}
81	2026-08-09 01:09:39.108453+09	\N	manual_input.create_report	trn_report	157	作成	報告書登録: report_code=RPT-0040, status=登録済み	\N	{"status": "登録済み", "summary": "ECサイト構築相談", "form_code": "G-3", "report_date": "2026-03-02"}
82	2026-08-09 01:09:39.110111+09	\N	manual_input.create_report	trn_report	158	作成	報告書登録: report_code=RPT-0041, status=登録済み	\N	{"status": "登録済み", "summary": "最低賃金引上げへの対応相談", "form_code": "G-8", "report_date": "2026-05-18"}
83	2026-08-09 01:09:39.111929+09	\N	manual_input.create_report	trn_report	159	作成	報告書登録: report_code=RPT-0042, status=登録済み	\N	{"status": "登録済み", "summary": "省エネ設備導入相談", "form_code": "G-3", "report_date": "2026-07-08"}
84	2026-08-09 01:09:39.113349+09	\N	manual_input.create_report	trn_report	160	作成	報告書登録: report_code=RPT-0043, status=登録済み	\N	{"status": "登録済み", "summary": "キャッシュレス導入相談", "form_code": "F", "report_date": "2026-06-11"}
85	2026-08-09 01:09:39.114919+09	\N	manual_input.create_report	trn_report	161	作成	報告書登録: report_code=RPT-0044, status=登録済み	\N	{"status": "登録済み", "summary": "キャッシュレス導入相談", "form_code": "G-3", "report_date": "2026-06-23"}
86	2026-08-09 01:09:39.118394+09	\N	manual_input.create_report	trn_report	162	作成	報告書登録: report_code=RPT-0045, status=登録済み	\N	{"status": "登録済み", "summary": "関税影響試算の相談", "form_code": "G-7", "report_date": "2026-02-11"}
87	2026-08-09 01:09:39.121091+09	\N	manual_input.create_report	trn_report	163	作成	報告書登録: report_code=RPT-0046, status=登録済み	\N	{"status": "登録済み", "summary": "免税事業者取引の相談", "form_code": "G-4", "report_date": "2026-04-09"}
88	2026-08-09 01:09:39.122751+09	\N	manual_input.create_report	trn_report	164	作成	報告書登録: report_code=RPT-0047, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "F", "report_date": "2026-03-06"}
89	2026-08-09 01:09:39.124292+09	\N	manual_input.create_report	trn_report	165	作成	報告書登録: report_code=RPT-0048, status=登録済み	\N	{"status": "登録済み", "summary": "新商品開発の相談", "form_code": "G-6", "report_date": "2026-07-18"}
90	2026-08-09 01:09:39.125842+09	\N	manual_input.create_report	trn_report	166	作成	報告書登録: report_code=RPT-0049, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "G-4", "report_date": "2026-01-11"}
91	2026-08-09 01:09:39.127702+09	\N	manual_input.create_report	trn_report	167	作成	報告書登録: report_code=RPT-0050, status=登録済み	\N	{"status": "登録済み", "summary": "キャッシュレス導入相談", "form_code": "F", "report_date": "2025-12-23"}
92	2026-08-09 01:09:39.129451+09	\N	manual_input.create_report	trn_report	168	作成	報告書登録: report_code=RPT-0051, status=登録済み	\N	{"status": "登録済み", "summary": "輸出先多角化の相談", "form_code": "G-4", "report_date": "2026-03-16"}
93	2026-08-09 01:09:39.130911+09	\N	manual_input.create_report	trn_report	169	作成	報告書登録: report_code=RPT-0052, status=登録済み	\N	{"status": "登録済み", "summary": "省エネ設備導入相談", "form_code": "G-4", "report_date": "2026-03-26"}
94	2026-08-09 01:09:39.13356+09	\N	manual_input.create_report	trn_report	170	作成	報告書登録: report_code=RPT-0053, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁交渉の相談", "form_code": "G-6", "report_date": "2026-01-14"}
95	2026-08-09 01:09:39.135794+09	\N	manual_input.create_report	trn_report	171	作成	報告書登録: report_code=RPT-0054, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "G-2", "report_date": "2026-04-20"}
96	2026-08-09 01:09:39.137775+09	\N	manual_input.create_report	trn_report	172	作成	報告書登録: report_code=RPT-0055, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁の進め方相談", "form_code": "G-5", "report_date": "2026-04-12"}
97	2026-08-09 01:09:39.13958+09	\N	manual_input.create_report	trn_report	173	作成	報告書登録: report_code=RPT-0056, status=登録済み	\N	{"status": "登録済み", "summary": "コロナ融資返済相談", "form_code": "G-8", "report_date": "2026-06-13"}
98	2026-08-09 01:09:39.141477+09	\N	manual_input.create_report	trn_report	174	作成	報告書登録: report_code=RPT-0057, status=登録済み	\N	{"status": "登録済み", "summary": "業務フロー見直し相談", "form_code": "G-7", "report_date": "2026-04-12"}
99	2026-08-09 01:09:39.14291+09	\N	manual_input.create_report	trn_report	175	作成	報告書登録: report_code=RPT-0058, status=登録済み	\N	{"status": "登録済み", "summary": "実績報告準備の相談", "form_code": "G-3", "report_date": "2026-01-01"}
100	2026-08-09 01:09:39.144447+09	\N	manual_input.create_report	trn_report	176	作成	報告書登録: report_code=RPT-0059, status=登録済み	\N	{"status": "登録済み", "summary": "クラウド会計導入相談", "form_code": "G-2", "report_date": "2026-02-20"}
101	2026-08-09 01:09:39.146204+09	\N	manual_input.create_report	trn_report	177	作成	報告書登録: report_code=RPT-0060, status=登録済み	\N	{"status": "登録済み", "summary": "輸出先多角化の相談", "form_code": "G-2", "report_date": "2026-07-19"}
102	2026-08-09 01:09:39.147601+09	\N	manual_input.create_report	trn_report	178	作成	報告書登録: report_code=RPT-0061, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "G-4", "report_date": "2026-03-04"}
103	2026-08-09 01:09:39.152313+09	\N	manual_input.create_report	trn_report	179	作成	報告書登録: report_code=RPT-0062, status=登録済み	\N	{"status": "登録済み", "summary": "事業再構築の相談", "form_code": "G-5", "report_date": "2026-05-23"}
104	2026-08-09 01:09:39.154376+09	\N	manual_input.create_report	trn_report	180	作成	報告書登録: report_code=RPT-0063, status=登録済み	\N	{"status": "登録済み", "summary": "クラウド会計導入相談", "form_code": "G-2", "report_date": "2026-02-21"}
105	2026-08-09 01:09:39.157416+09	\N	manual_input.create_report	trn_report	181	作成	報告書登録: report_code=RPT-0064, status=登録済み	\N	{"status": "登録済み", "summary": "省エネ設備導入相談", "form_code": "G-2", "report_date": "2026-02-11"}
106	2026-08-09 01:09:39.159532+09	\N	manual_input.create_report	trn_report	182	作成	報告書登録: report_code=RPT-0065, status=登録済み	\N	{"status": "登録済み", "summary": "免税事業者取引の相談", "form_code": "F", "report_date": "2026-03-08"}
107	2026-08-09 01:09:39.16118+09	\N	manual_input.create_report	trn_report	183	作成	報告書登録: report_code=RPT-0066, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "G-4", "report_date": "2026-01-03"}
108	2026-08-09 01:09:39.162596+09	\N	manual_input.create_report	trn_report	184	作成	報告書登録: report_code=RPT-0067, status=登録済み	\N	{"status": "登録済み", "summary": "関税影響試算の相談", "form_code": "G-4", "report_date": "2026-04-04"}
109	2026-08-09 01:09:39.164057+09	\N	manual_input.create_report	trn_report	185	作成	報告書登録: report_code=RPT-0068, status=登録済み	\N	{"status": "登録済み", "summary": "実績報告準備の相談", "form_code": "G-6", "report_date": "2026-06-03"}
110	2026-08-09 01:09:39.166469+09	\N	manual_input.create_report	trn_report	186	作成	報告書登録: report_code=RPT-0069, status=登録済み	\N	{"status": "登録済み", "summary": "省エネ設備導入相談", "form_code": "G-6", "report_date": "2026-07-18"}
111	2026-08-09 01:09:39.168721+09	\N	manual_input.create_report	trn_report	187	作成	報告書登録: report_code=RPT-0070, status=登録済み	\N	{"status": "登録済み", "summary": "タイムスタンプ要件の相談", "form_code": "G-4", "report_date": "2026-01-31"}
112	2026-08-09 01:09:39.170896+09	\N	manual_input.create_report	trn_report	188	作成	報告書登録: report_code=RPT-0071, status=登録済み	\N	{"status": "登録済み", "summary": "実績報告準備の相談", "form_code": "G-7", "report_date": "2026-06-19"}
113	2026-08-09 01:09:39.172685+09	\N	manual_input.create_report	trn_report	189	作成	報告書登録: report_code=RPT-0072, status=登録済み	\N	{"status": "登録済み", "summary": "免税事業者取引の相談", "form_code": "G-7", "report_date": "2025-12-24"}
114	2026-08-09 01:09:39.174256+09	\N	manual_input.create_report	trn_report	190	作成	報告書登録: report_code=RPT-0073, status=登録済み	\N	{"status": "登録済み", "summary": "価格交渉の相談", "form_code": "F", "report_date": "2026-06-28"}
115	2026-08-09 01:09:39.176417+09	\N	manual_input.create_report	trn_report	191	作成	報告書登録: report_code=RPT-0074, status=登録済み	\N	{"status": "登録済み", "summary": "最低賃金引上げへの対応相談", "form_code": "F", "report_date": "2026-04-25"}
116	2026-08-09 01:09:39.178253+09	\N	manual_input.create_report	trn_report	192	作成	報告書登録: report_code=RPT-0075, status=登録済み	\N	{"status": "登録済み", "summary": "コロナ融資返済相談", "form_code": "G-3", "report_date": "2025-08-18"}
117	2026-08-09 01:09:39.180403+09	\N	manual_input.create_report	trn_report	193	作成	報告書登録: report_code=RPT-0076, status=登録済み	\N	{"status": "登録済み", "summary": "省力化補助金の活用相談", "form_code": "G-6", "report_date": "2025-11-24"}
118	2026-08-09 01:09:39.185177+09	\N	manual_input.create_report	trn_report	194	作成	報告書登録: report_code=RPT-0077, status=登録済み	\N	{"status": "登録済み", "summary": "電力契約見直し相談", "form_code": "G-4", "report_date": "2025-11-16"}
119	2026-08-09 01:09:39.188186+09	\N	manual_input.create_report	trn_report	195	作成	報告書登録: report_code=RPT-0078, status=登録済み	\N	{"status": "登録済み", "summary": "経理体制整備の相談", "form_code": "G-2", "report_date": "2026-01-09"}
120	2026-08-09 01:09:39.19191+09	\N	manual_input.create_report	trn_report	196	作成	報告書登録: report_code=RPT-0079, status=登録済み	\N	{"status": "登録済み", "summary": "関税影響試算の相談", "form_code": "G-2", "report_date": "2026-04-23"}
121	2026-08-09 01:09:39.194279+09	\N	manual_input.create_report	trn_report	197	作成	報告書登録: report_code=RPT-0080, status=登録済み	\N	{"status": "登録済み", "summary": "コロナ融資返済相談", "form_code": "G-6", "report_date": "2026-05-22"}
122	2026-08-09 01:09:39.196967+09	\N	manual_input.create_report	trn_report	198	作成	報告書登録: report_code=RPT-0081, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "G-5", "report_date": "2026-04-22"}
123	2026-08-09 01:09:39.202632+09	\N	manual_input.create_report	trn_report	199	作成	報告書登録: report_code=RPT-0082, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "G-4", "report_date": "2025-12-29"}
124	2026-08-09 01:09:39.20486+09	\N	manual_input.create_report	trn_report	200	作成	報告書登録: report_code=RPT-0083, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "F", "report_date": "2026-02-18"}
125	2026-08-09 01:09:39.206666+09	\N	manual_input.create_report	trn_report	201	作成	報告書登録: report_code=RPT-0084, status=登録済み	\N	{"status": "登録済み", "summary": "価格転嫁交渉の相談", "form_code": "G-8", "report_date": "2026-05-17"}
126	2026-08-09 01:09:39.208607+09	\N	manual_input.create_report	trn_report	202	作成	報告書登録: report_code=RPT-0085, status=登録済み	\N	{"status": "登録済み", "summary": "関税影響試算の相談", "form_code": "G-4", "report_date": "2026-01-12"}
127	2026-08-09 01:09:39.210322+09	\N	manual_input.create_report	trn_report	203	作成	報告書登録: report_code=RPT-0086, status=登録済み	\N	{"status": "登録済み", "summary": "輸出先多角化の相談", "form_code": "G-2", "report_date": "2026-01-12"}
128	2026-08-09 01:09:39.212761+09	\N	manual_input.create_report	trn_report	204	作成	報告書登録: report_code=RPT-0087, status=登録済み	\N	{"status": "登録済み", "summary": "キャッシュレス導入相談", "form_code": "G-7", "report_date": "2025-09-05"}
129	2026-08-09 01:09:39.215024+09	\N	manual_input.create_report	trn_report	205	作成	報告書登録: report_code=RPT-0088, status=登録済み	\N	{"status": "登録済み", "summary": "新商品開発の相談", "form_code": "G-8", "report_date": "2025-10-15"}
130	2026-08-09 01:09:39.219484+09	\N	manual_input.create_report	trn_report	206	作成	報告書登録: report_code=RPT-0089, status=登録済み	\N	{"status": "登録済み", "summary": "省力化補助金の活用相談", "form_code": "G-2", "report_date": "2026-07-20"}
131	2026-08-09 01:09:39.222161+09	\N	manual_input.create_report	trn_report	207	作成	報告書登録: report_code=RPT-0090, status=登録済み	\N	{"status": "登録済み", "summary": "スキャナ保存の相談", "form_code": "G-8", "report_date": "2025-11-03"}
132	2026-08-09 01:09:39.224554+09	\N	manual_input.create_report	trn_report	208	作成	報告書登録: report_code=RPT-0091, status=登録済み	\N	{"status": "登録済み", "summary": "新商品開発の相談", "form_code": "G-5", "report_date": "2025-12-23"}
133	2026-08-09 01:09:39.226425+09	\N	manual_input.create_report	trn_report	209	作成	報告書登録: report_code=RPT-0092, status=登録済み	\N	{"status": "登録済み", "summary": "電子取引データ保存の相談", "form_code": "G-3", "report_date": "2025-10-04"}
134	2026-08-09 01:09:39.228493+09	\N	manual_input.create_report	trn_report	210	作成	報告書登録: report_code=RPT-0093, status=登録済み	\N	{"status": "登録済み", "summary": "賃上げ実施時期の相談", "form_code": "G-8", "report_date": "2026-07-01"}
135	2026-08-09 01:09:49.71763+09	1	accounts.update	mst_user_account	89	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "011", "shokuin_kj": "北海道\\t一般職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "011@011.011.011", "status": 1, "user_id": "011", "shokuin_kj": "北海道\\t一般職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}
136	2026-08-09 01:10:00.408078+09	1	accounts.update	mst_user_account	90	更新	\N	{"email": "mail@mail.mail.mail", "status": 1, "user_id": "012", "shokuin_kj": "北海道商工会権限", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "県連（商工会権限）"}	{"email": "012@012.012.012", "status": 1, "user_id": "012", "shokuin_kj": "北海道商工会権限", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "県連（商工会権限）"}
137	2026-08-09 01:11:21.680332+09	1	accounts.update	mst_user_account	12	更新	\N	{"email": "tanaka@ishikarikita.example.jp", "status": 1, "user_id": "ST-201", "shokuin_kj": "田中 一郎", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "0100@0100.0100.0100", "status": 1, "user_id": "0100", "shokuin_kj": "商工会管理者", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "管理者"}
138	2026-08-09 01:11:55.708498+09	1	accounts.update	mst_user_account	13	更新	\N	{"email": "suzuki@hakodatehigashi.example.jp", "status": 1, "user_id": "ST-202", "shokuin_kj": "鈴木 次郎", "shokokai_cd": "2005", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "suzuki@hakodatehigashi.example.jp", "status": 1, "user_id": "0101", "shokuin_kj": "商工会一般", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}
139	2026-08-09 01:12:16.596206+09	1	accounts.update	mst_user_account	89	更新	\N	{"email": "011@011.011.011", "status": 1, "user_id": "011", "shokuin_kj": "北海道\\t一般職員", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "011@011.011.011", "status": 1, "user_id": "011", "shokuin_kj": "北海道一般", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}
140	2026-08-09 01:12:27.101556+09	1	accounts.update	mst_user_account	91	更新	\N	{"email": "001@001.001.001", "status": 1, "user_id": "001", "shokuin_kj": "全国連一般職員", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}	{"email": "001@001.001.001", "status": 1, "user_id": "001", "shokuin_kj": "全国連一般", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}
141	2026-08-09 01:12:54.285297+09	1	accounts.update	mst_user_account	12	更新	\N	{"email": "0100@0100.0100.0100", "status": 1, "user_id": "0100", "shokuin_kj": "商工会管理者", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "管理者"}	{"email": "013@013.013.013", "status": 1, "user_id": "013", "shokuin_kj": "商工会管理者", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "管理者"}
142	2026-08-09 01:13:13.276042+09	1	accounts.update	mst_user_account	13	更新	\N	{"email": "suzuki@hakodatehigashi.example.jp", "status": 1, "user_id": "0101", "shokuin_kj": "商工会一般", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "014@014.014.014", "status": 1, "user_id": "014", "shokuin_kj": "商工会一般", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}
143	2026-08-09 01:47:56.826689+09	1	knowledge.create_entry	trn_knowledge_entry	15	作成	知識データ登録: knowledge_code=KN-013, status=下書き	\N	{"title": "テスト_適用範囲確認", "status": "下書き", "knowledge_document_id": null}
144	2026-08-09 01:50:40.571697+09	1	knowledge.create_document	mst_knowledge_document	13	作成	文書登録: document_code=doc-010, title=テスト文書_全県確認	\N	{"title": "テスト文書_全県確認", "format": "PDF", "category": "賃上げ関連", "prefecture_code": null}
145	2026-08-09 10:06:52.856437+09	90	manual_input.create_report	trn_report	211	作成	報告書登録: report_code=RPT-0094, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-09"}
146	2026-08-09 10:07:24.491942+09	90	manual_input.update_report	trn_report	211	更新	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-09"}	{"status": "登録済み", "summary": "内容", "form_code": "F", "report_date": "2026-08-09"}
147	2026-08-12 14:58:25.61188+09	90	manual_input.create_report	trn_report	212	作成	報告書登録: report_code=RPT-0095, status=登録済み	\N	{"status": "登録済み", "summary": "概要", "form_code": "G-2", "report_date": "2026-08-12"}
148	2026-08-12 20:27:14.835337+09	1	accounts.create	mst_user_account	93	作成	アカウント作成: user_id=QTEST01, permission_level=一般職員	\N	{"email": "qtest01@example.jp", "status": 1, "user_id": "QTEST01", "shokuin_kj": "テスト太郎", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}
149	2026-08-12 20:27:14.910109+09	1	accounts.update	mst_user_account	93	更新	\N	{"email": "qtest01@example.jp", "status": 1, "user_id": "QTEST01", "shokuin_kj": "テスト太郎", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "qtest01@example.jp", "status": 1, "user_id": "QTEST01", "shokuin_kj": "テスト太郎", "shokokai_cd": "2001", "prefecture_code": "01", "permission_level": "一般職員"}
150	2026-08-13 07:00:16.584656+09	22	manual_input.create_report	trn_report	213	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "G-3のテスト内容", "form_code": "G-3", "report_date": "2026-08-12"}
151	2026-08-13 07:00:16.692705+09	22	manual_input.create_report	trn_report	214	作成	報告書登録: report_code=RPT-0097, status=登録済み	\N	{"status": "登録済み", "summary": "G-4のテスト内容", "form_code": "G-4", "report_date": "2026-08-12"}
152	2026-08-13 07:00:16.722361+09	22	manual_input.create_report	trn_report	215	作成	報告書登録: report_code=RPT-0098, status=登録済み	\N	{"status": "登録済み", "summary": "G-6のテスト内容", "form_code": "G-6", "report_date": "2026-08-12"}
153	2026-08-13 07:00:16.752605+09	22	manual_input.create_report	trn_report	216	作成	報告書登録: report_code=RPT-0099, status=登録済み	\N	{"status": "登録済み", "summary": "G-7のテスト内容", "form_code": "G-7", "report_date": "2026-08-12"}
154	2026-08-13 07:00:16.921497+09	22	manual_input.create_report	trn_report	217	作成	報告書登録: report_code=RPT-0100, status=登録済み	\N	{"status": "登録済み", "summary": "G-2のテスト内容", "form_code": "G-2", "report_date": "2026-08-12"}
155	2026-08-13 07:00:16.957979+09	22	manual_input.create_report	trn_report	218	作成	報告書登録: report_code=RPT-0101, status=登録済み	\N	{"status": "登録済み", "summary": "G-2のテスト内容", "form_code": "G-2", "report_date": "2026-08-12"}
156	2026-08-13 07:00:46.242201+09	22	manual_input.create_report	trn_report	219	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
157	2026-08-13 07:00:46.297119+09	22	manual_input.create_report	trn_report	220	作成	報告書登録: report_code=RPT-0097, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
158	2026-08-13 07:00:46.329645+09	22	manual_input.create_report	trn_report	221	作成	報告書登録: report_code=RPT-0098, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
159	2026-08-13 07:00:46.362327+09	22	manual_input.create_report	trn_report	222	作成	報告書登録: report_code=RPT-0099, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
160	2026-08-13 07:00:46.39446+09	22	manual_input.create_report	trn_report	223	作成	報告書登録: report_code=RPT-0100, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
161	2026-08-13 07:00:46.418103+09	22	manual_input.create_report	trn_report	224	作成	報告書登録: report_code=RPT-0101, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
162	2026-08-13 07:00:46.444136+09	22	manual_input.create_report	trn_report	225	作成	報告書登録: report_code=RPT-0102, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
163	2026-08-13 07:01:03.982209+09	22	manual_input.create_report	trn_report	226	作成	報告書登録: report_code=RPT-0103, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
164	2026-08-13 07:01:04.035097+09	22	manual_input.create_report	trn_report	227	作成	報告書登録: report_code=RPT-0104, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
165	2026-08-13 07:01:04.064982+09	22	manual_input.create_report	trn_report	228	作成	報告書登録: report_code=RPT-0105, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
166	2026-08-13 07:01:04.092121+09	22	manual_input.create_report	trn_report	229	作成	報告書登録: report_code=RPT-0106, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
167	2026-08-13 07:01:04.124227+09	22	manual_input.create_report	trn_report	230	作成	報告書登録: report_code=RPT-0107, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
168	2026-08-13 07:01:04.155355+09	22	manual_input.create_report	trn_report	231	作成	報告書登録: report_code=RPT-0108, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
169	2026-08-13 07:01:04.187155+09	22	manual_input.create_report	trn_report	232	作成	報告書登録: report_code=RPT-0109, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-2", "report_date": "2026-08-13"}
170	2026-08-13 09:22:59.645604+09	22	manual_input.create_report	trn_report	233	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "Fのテスト内容", "form_code": "F", "report_date": "2026-08-13"}
171	2026-08-13 09:22:59.750863+09	22	manual_input.create_report	trn_report	234	作成	報告書登録: report_code=RPT-0097, status=登録済み	\N	{"status": "登録済み", "summary": "G-8のテスト内容", "form_code": "G-8", "report_date": "2026-08-13"}
172	2026-08-13 09:25:41.255292+09	90	manual_input.update_report	trn_report	211	更新	\N	{"status": "登録済み", "summary": "内容", "form_code": "F", "report_date": "2026-08-09"}	{"status": "登録済み", "summary": "内容", "form_code": "G-7", "report_date": "2026-08-09"}
173	2026-08-13 09:28:51.245189+09	22	manual_input.create_report	trn_report	235	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "G-3内容", "form_code": "G-3", "report_date": "2026-08-13"}
174	2026-08-13 09:28:51.279157+09	22	manual_input.create_report	trn_report	236	作成	報告書登録: report_code=RPT-0097, status=登録済み	\N	{"status": "登録済み", "summary": "G-4内容", "form_code": "G-4", "report_date": "2026-08-13"}
175	2026-08-13 09:40:47.779614+09	22	manual_input.create_report	trn_report	237	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "G-6内容", "form_code": "G-6", "report_date": "2026-08-13"}
176	2026-08-13 09:40:47.805494+09	22	manual_input.create_report	trn_report	238	作成	報告書登録: report_code=RPT-0097, status=登録済み	\N	{"status": "登録済み", "summary": "G-4内容", "form_code": "G-4", "report_date": "2026-08-13"}
177	2026-08-14 12:48:34.787961+09	22	manual_input.create_report	trn_report	239	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-3", "report_date": "2026-08-13"}
178	2026-08-14 12:57:32.075072+09	22	manual_input.create_report	trn_report	240	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "G-3内容", "form_code": "G-3", "report_date": "2026-08-13"}
179	2026-08-14 12:57:32.131604+09	22	manual_input.create_report	trn_report	241	作成	報告書登録: report_code=RPT-0097, status=登録済み	\N	{"status": "登録済み", "summary": "G-4内容", "form_code": "G-4", "report_date": "2026-08-13"}
180	2026-08-14 16:35:34.854019+09	22	manual_input.create_report	trn_report	213	作成	報告書登録: report_code=RPT-0096, status=登録済み	\N	{"status": "登録済み", "summary": "内容", "form_code": "G-3", "report_date": "2026-08-14"}
181	2026-08-26 22:38:33.765523+09	90	manual_input.create_report	trn_report	239	作成	報告書登録: report_code=RPT-0121, status=下書き	\N	{"status": "下書き", "summary": "", "form_code": null, "report_date": "2026-08-26"}
182	2026-08-26 22:46:10.417366+09	90	manual_input.create_report	trn_report	240	作成	報告書登録: report_code=RPT-0122, status=下書き	\N	{"status": "下書き", "summary": "", "form_code": null, "report_date": "2026-08-26"}
183	2026-08-27 07:14:00.158001+09	22	manual_input.create_report	trn_report	241	作成	報告書登録: report_code=RPT-0123, status=登録済み	\N	{"status": "登録済み", "summary": "Playwright検証用の相談内容です。", "form_code": "F", "report_date": "2026-08-20"}
184	2026-08-27 07:14:01.293103+09	22	manual_input.create_report	trn_report	242	作成	報告書登録: report_code=RPT-0124, status=登録済み	\N	{"status": "登録済み", "summary": "Playwright検証用のG-2報告内容です。", "form_code": "G-2", "report_date": "2026-08-20"}
185	2026-08-27 07:14:05.594296+09	22	manual_input.update_report	trn_report	242	更新	status: 登録済み → 下書き	{"status": "登録済み", "summary": "Playwright検証用のG-2報告内容です。", "form_code": "G-2", "report_date": "2026-08-20"}	{"status": "下書き", "summary": "Playwright検証用のG-2報告内容です。", "form_code": "G-2", "report_date": "2026-08-20"}
186	2026-08-27 07:14:42.755597+09	22	manual_input.create_report	trn_report	243	作成	報告書登録: report_code=RPT-0125, status=登録済み	\N	{"status": "登録済み", "summary": "manual-inputから様式Fを新規作成", "form_code": "F", "report_date": "2026-08-21"}
187	2026-08-27 07:14:43.444233+09	22	manual_input.update_report	trn_report	243	更新	\N	{"status": "登録済み", "summary": "manual-inputから様式Fを新規作成", "form_code": "F", "report_date": "2026-08-21"}	{"status": "登録済み", "summary": "様式切替後の内容", "form_code": "G-2", "report_date": "2026-08-21"}
188	2026-08-27 07:15:04.40126+09	22	manual_input.delete_report	trn_report	241	削除	報告書削除（論理削除）: report_code=RPT-0123	{"status": "登録済み", "content": "Playwright検証用の相談内容です。", "summary": "Playwright検証用の相談内容です。", "location": null, "theme_id": 13, "time_end": "11:00", "form_code": "F", "report_id": 241, "created_at": "20260827071400", "created_by": 22, "deleted_at": null, "deleted_by": null, "printed_at": null, "time_start": "10:00", "updated_at": "20260827071400", "updated_by": 22, "venue_name": null, "expert_name": null, "report_code": "RPT-0123", "report_date": "2026-08-20", "shokokai_cd": "2001", "business_name": "テスト商店_PWCHECK", "current_issue": null, "industry_code": "I", "registered_at": "2026-08-27", "attendee_count": null, "fiscal_year_id": 3, "industry_label": "卸売業、小売業", "staff_sub_name": null, "support_result": null, "business_person": "", "form_full_label": "F 相談受付票", "prefecture_code": "20", "staff_main_name": "井上 直樹", "support_content": null, "visit_result_id": null, "capital_range_id": null, "revenue_range_id": null, "voice_transcript": null, "employee_range_id": null, "primary_theme_code": "wage", "visit_result_label": null, "capital_range_label": null, "revenue_range_label": null, "employee_range_label": null, "expert_qualification_id": null, "expert_qualification_label": null}	\N
189	2026-08-27 07:15:05.754626+09	22	manual_input.delete_report	trn_report	242	削除	報告書削除（論理削除）: report_code=RPT-0124	{"status": "下書き", "content": "Playwright検証用のG-2報告内容です。", "summary": "Playwright検証用のG-2報告内容です。", "location": null, "theme_id": 13, "time_end": "14:00", "form_code": "G-2", "report_id": 242, "created_at": "20260827071401", "created_by": 22, "deleted_at": null, "deleted_by": null, "printed_at": null, "time_start": "13:00", "updated_at": "20260827071405", "updated_by": 22, "venue_name": null, "expert_name": null, "report_code": "RPT-0124", "report_date": "2026-08-20", "shokokai_cd": "2001", "business_name": "テスト商店_PWCHECK", "current_issue": null, "industry_code": "I", "registered_at": "2026-08-27", "attendee_count": null, "fiscal_year_id": 3, "industry_label": "卸売業、小売業", "staff_sub_name": null, "support_result": null, "business_person": "", "form_full_label": "G-2 専門家相談員報告書", "prefecture_code": "20", "staff_main_name": "井上 直樹", "support_content": null, "visit_result_id": null, "capital_range_id": null, "revenue_range_id": null, "voice_transcript": null, "employee_range_id": null, "primary_theme_code": "wage", "visit_result_label": null, "capital_range_label": null, "revenue_range_label": null, "employee_range_label": null, "expert_qualification_id": null, "expert_qualification_label": null}	\N
190	2026-08-27 07:15:07.061676+09	22	manual_input.delete_report	trn_report	243	削除	報告書削除（論理削除）: report_code=RPT-0125	{"status": "登録済み", "content": "様式切替後の内容", "summary": "様式切替後の内容", "location": null, "theme_id": 13, "time_end": "09:30", "form_code": "G-2", "report_id": 243, "created_at": "20260827071442", "created_by": 22, "deleted_at": null, "deleted_by": null, "printed_at": null, "time_start": "09:00", "updated_at": "20260827071443", "updated_by": 22, "venue_name": null, "expert_name": null, "report_code": "RPT-0125", "report_date": "2026-08-21", "shokokai_cd": "2001", "business_name": "テスト商店_PWCHECK2", "current_issue": null, "industry_code": "I", "registered_at": "2026-08-27", "attendee_count": null, "fiscal_year_id": 3, "industry_label": "卸売業、小売業", "staff_sub_name": null, "support_result": null, "business_person": "", "form_full_label": "G-2 専門家相談員報告書", "prefecture_code": "20", "staff_main_name": "井上 直樹", "support_content": null, "visit_result_id": null, "capital_range_id": null, "revenue_range_id": null, "voice_transcript": null, "employee_range_id": null, "primary_theme_code": "wage", "visit_result_label": null, "capital_range_label": null, "revenue_range_label": null, "employee_range_label": null, "expert_qualification_id": null, "expert_qualification_label": null}	\N
191	2026-08-27 07:18:32.77689+09	90	manual_input.create_report	trn_report	244	作成	報告書登録: report_code=RPT-0126, status=下書き	\N	{"status": "下書き", "summary": "", "form_code": null, "report_date": "2026-08-27"}
192	2026-08-27 07:29:31.472254+09	1	accounts.update	mst_user_account	89	更新	permission_level: 一般職員 → 管理者	{"email": "011@011.011.011", "status": 1, "user_id": "011", "shokuin_kj": "増田 大輔", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "一般職員"}	{"email": "011@011.011.011", "status": 1, "user_id": "011", "shokuin_kj": "増田 大輔", "shokokai_cd": "0021", "prefecture_code": "01", "permission_level": "管理者"}
193	2026-08-27 07:31:31.465196+09	22	manual_input.update_report	trn_report	163	更新	status: 登録済み → 下書き	{"status": "登録済み", "summary": "免税事業者取引の相談", "form_code": "G-4", "report_date": "2026-04-09"}	{"status": "下書き", "summary": "免税事業者との取引条件について相談があり、下請取引の留意点を助言した。", "form_code": "G-4", "report_date": "2026-04-09"}
194	2026-08-27 07:31:33.565986+09	22	manual_input.update_report	trn_report	163	更新	\N	{"status": "下書き", "summary": "免税事業者との取引条件について相談があり、下請取引の留意点を助言した。", "form_code": "G-4", "report_date": "2026-04-09"}	{"status": "下書き", "summary": "免税事業者との取引条件について相談があり、下請取引の留意点を助言した。", "form_code": "G-4", "report_date": "2026-04-09"}
195	2026-08-27 07:33:35.306606+09	22	manual_input.create_report	trn_report	245	作成	報告書登録: report_code=RPT-0127, status=登録済み	\N	{"status": "登録済み", "summary": "multipart化後の新規作成テスト", "form_code": "G-2", "report_date": "2026-08-22"}
196	2026-08-27 07:33:36.058477+09	22	manual_input.update_report	trn_report	245	更新	\N	{"status": "登録済み", "summary": "multipart化後の新規作成テスト", "form_code": "G-2", "report_date": "2026-08-22"}	{"status": "登録済み", "summary": "編集して登録するテスト", "form_code": "G-2", "report_date": "2026-08-22"}
197	2026-08-27 07:33:36.785583+09	22	manual_input.delete_report	trn_report	245	削除	報告書削除（論理削除）: report_code=RPT-0127	{"status": "登録済み", "content": "編集して登録するテスト", "summary": "編集して登録するテスト", "location": null, "theme_id": 13, "time_end": "11:00", "form_code": "G-2", "report_id": 245, "created_at": "20260827073335", "created_by": 22, "deleted_at": null, "deleted_by": null, "printed_at": null, "time_start": "10:00", "updated_at": "20260827073336", "updated_by": 22, "venue_name": null, "expert_name": null, "report_code": "RPT-0127", "report_date": "2026-08-22", "shokokai_cd": "2001", "business_name": "回帰テスト商店", "current_issue": null, "industry_code": "I", "registered_at": "2026-08-27", "attendee_count": null, "fiscal_year_id": 3, "industry_label": "卸売業、小売業", "staff_sub_name": null, "support_result": null, "business_person": "", "form_full_label": "G-2 専門家相談員報告書", "prefecture_code": "20", "staff_main_name": "井上 直樹", "support_content": null, "visit_result_id": null, "capital_range_id": null, "revenue_range_id": null, "voice_transcript": null, "employee_range_id": null, "primary_theme_code": "wage", "visit_result_label": null, "capital_range_label": null, "revenue_range_label": null, "employee_range_label": null, "expert_qualification_id": null, "expert_qualification_label": null}	\N
198	2026-08-27 12:23:30.529494+09	1	accounts.update	mst_user_account	91	更新	\N	{"email": "001@001.001.001", "status": 1, "user_id": "001", "shokuin_kj": "平野 拓也", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}	{"email": "001@001.001.001", "status": 1, "user_id": "001", "shokuin_kj": "平野 拓也", "shokokai_cd": "0021", "prefecture_code": "00", "permission_level": "一般職員"}
199	2026-08-27 13:39:38.815611+09	16	accounts.create	mst_user_account	94	作成	アカウント作成: user_id=TEST-INLINE-01, permission_level=一般職員	\N	{"email": "test-inline@example.jp", "status": 1, "user_id": "TEST-INLINE-01", "shokuin_kj": "テスト太郎", "shokokai_cd": "2041", "prefecture_code": "01", "permission_level": "一般職員"}
200	2026-08-27 13:39:40.411285+09	16	accounts.delete	mst_user_account	94	削除	アカウント削除: user_id=TEST-INLINE-01	{"email": "test-inline@example.jp", "status": 1, "user_id": "TEST-INLINE-01", "shokuin_kj": "テスト太郎", "core_linked": false, "shokokai_cd": "2041", "status_label": "利用中", "last_login_at": null, "shokokai_name": "三笠市商工会", "prefecture_code": "01", "prefecture_name": "北海道", "user_account_id": 94, "permission_level": "一般職員", "status_badge_class": "badge-status-ok", "qualification_codes": []}	\N
\.


--
-- Data for Name: trn_knowledge_document; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_knowledge_document (knowledge_document_id, prefecture_code, active_version_number, document_code, title, category, format, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
3	\N	1	doc-003	省力化投資補助金 申請の手引き	補助金	PDF	20260808115851	\N	20260808115851	\N	\N	\N
4	\N	2	doc-004	インボイス制度 実務対応マニュアル	税制	Word	20260808115851	\N	20260808115851	\N	\N	\N
5	\N	1	doc-005	事業承継ガイドライン 2026	経営支援	PDF	20260808115851	\N	20260808115851	\N	\N	\N
6	\N	1	doc-006	最低賃金改定 都道府県別一覧	法令・制度	Excel	20260808115851	\N	20260808115851	\N	\N	\N
7	\N	1	doc-007	電子帳簿保存法 対応チェックリスト	税制	PDF	20260808115851	\N	20260808115851	\N	\N	\N
8	\N	1	doc-008	専門家派遣事業 実施要領	補助金	PDF	20260808115851	\N	20260808115851	\N	\N	\N
9	\N	1	doc-009	テスト文書	税制	PDF	20260808115851	\N	20260808115851	\N	\N	\N
1	\N	1	doc-001	商工会法 逐条解説（令和6年版）	法令・制度	PDF	20260808115851	\N	20260809003734	1	\N	\N
2	\N	2	doc-002	賃上げ促進税制 Q&A集	税制	PDF	20260808115851	\N	20260809003806	1	\N	\N
\.


--
-- Data for Name: trn_knowledge_document_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_knowledge_document_version (knowledge_document_version_id, knowledge_document_id, version_number, uploaded_date, uploaded_by, file_size_kb, status, file_path, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	1	1	2026-04-02	事務局	1820	登録済み	1/9a681b130e0a42e49b90163b313f1d2b.pdf	20260808115851	\N	20260808115851	\N	\N	\N
2	2	1	2026-03-05	事務局	940	旧版	2/37c920ba3c9e4542ab2e87ad7b9b6342.pdf	20260808115851	\N	20260808115851	\N	\N	\N
3	2	2	2026-04-10	事務局	1120	登録済み	2/3e6ec647ae03409eb8f94ad610a62fb8.pdf	20260808115851	\N	20260808115851	\N	\N	\N
4	3	1	2026-04-18	経営支援部	2340	登録済み	3/1383e9b7d5ab4557b6ee52fb64842f57.pdf	20260808115851	\N	20260808115851	\N	\N	\N
5	4	1	2026-04-20	事務局	610	旧版	4/17a7fbbf8b4f4d938478376e535bec34.docx	20260808115851	\N	20260808115851	\N	\N	\N
6	4	2	2026-05-01	事務局	685	処理中	4/2f0101de4b5243ce9a29149d38ab7dbf.docx	20260808115851	\N	20260808115851	\N	\N	\N
7	5	1	2026-05-12	経営支援部	3120	登録済み	5/243ff5c3d12e4750813e21995626eee9.pdf	20260808115851	\N	20260808115851	\N	\N	\N
8	6	1	2026-05-20	事務局	128	登録済み	6/ce1ee0d7fde34232a3913dccc3a4f264.xlsx	20260808115851	\N	20260808115851	\N	\N	\N
9	7	1	2026-06-02	事務局	480	エラー	7/f1c12ff534a548838146c39503bcab3d.pdf	20260808115851	\N	20260808115851	\N	\N	\N
10	8	1	2026-06-15	経営支援部	890	登録済み	8/2bc88f0653fe41a3a6f5ea014536fe80.pdf	20260808115851	\N	20260808115851	\N	\N	\N
11	9	1	2026-08-03	山田 太郎	1	登録済み	9/c05d57a4f818458b9995cb3981d9fc2e.pdf	20260808115851	\N	20260808115851	\N	\N	\N
\.


--
-- Data for Name: trn_knowledge_entry; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_knowledge_entry (knowledge_entry_id, knowledge_document_id, prefecture_code, knowledge_code, title, updated_date, status, content, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
2	3	\N	KN-002	省力化投資補助金 対象設備の判定基準	2026-04-22	公開中	省力化投資補助金の対象設備は、人手不足の解消に直接寄与する汎用性の高い設備・システムであることが条件。カタログに登録された製品から選定する「カタログ型」と、個別の生産性向上計画に基づく「一般型」の2区分がある。補助率は中小企業で1/2、小規模事業者で2/3。補助上限額は従業員数に応じて200万円〜1,500万円。	20260808115851	\N	20260808115851	\N	\N	\N
3	4	\N	KN-003	インボイス発行事業者登録の手順	2026-05-05	下書き	適格請求書発行事業者になるには、納税地を所轄する税務署長に登録申請書を提出する。e-Taxでの電子申請も可能。免税事業者が登録する場合は課税事業者選択届出書の提出も必要（経過措置により省略可能な場合あり）。登録通知後、登録番号（T+13桁の数字）を請求書等に記載する。	20260808115851	\N	20260808115851	\N	\N	\N
4	5	\N	KN-004	事業承継税制の特例措置一覧	2026-05-16	公開中	法人版事業承継税制の特例措置では、非上場株式等に係る贈与税・相続税の納税猶予割合が100%となる。適用には特例承継計画を都道府県知事に提出し確認を受ける必要がある（提出期限あり）。承継後も雇用維持要件等の報告が必要だが、特例措置では要件を満たさない場合でも猶予継続が可能な柔軟性がある。	20260808115851	\N	20260808115851	\N	\N	\N
5	6	\N	KN-005	都道府県別 最低賃金改定額（令和8年度）	2026-05-24	公開中	令和8年度の地域別最低賃金改定額は、全国加重平均で前年度から数十円程度の引き上げとなる見込み。改定は例年10月頃に発効。都道府県ごとにランク分けされ、引き上げ額の目安が中央最低賃金審議会から示された後、各地方最低賃金審議会が地域の実情を踏まえて決定する。	20260808115851	\N	20260808115851	\N	\N	\N
6	7	\N	KN-006	電子帳簿保存法 保存要件のチェックポイント	2026-06-05	下書き	電子取引データの保存要件は、①改ざん防止措置（タイムスタンプ付与や事務処理規程の整備等）、②日付・金額・取引先で検索できる状態の確保、③ディスプレイ・プリンタ等の備付け、の3点。検索要件は判定期間の売上高が一定額以下の事業者等は緩和措置がある。	20260808115851	\N	20260808115851	\N	\N	\N
7	8	\N	KN-007	専門家派遣事業 申込フロー	2026-06-18	公開中	専門家派遣を希望する事業者は、まず商工会の窓口で相談内容を伝え、派遣が必要と判断された場合に申込書を提出する。商工会が専門家（中小企業診断士・税理士等）を選定・調整し、日程確定後に派遣が実施される。派遣後は報告書（様式G-4）を専門家が作成し提出する。	20260808115851	\N	20260808115851	\N	\N	\N
8	1	\N	KN-008	商工会法における組織運営の基本	2026-04-08	公開中	商工会は商工会法に基づき設立される特別認可法人。地区内の商工業者を会員とし、総会（または総代会）を最高意思決定機関とする。役員として会長・副会長・理事・監事を置く。経営改善普及事業（経営指導）を主たる事業とし、都道府県・国の補助を受けて運営される。	20260808115851	\N	20260808115851	\N	\N	\N
9	\N	\N	KN-009	テストエントリ	2026-08-03	下書き	テスト本文	20260808115851	\N	20260808115851	\N	\N	\N
10	\N	\N	KN-010	リファクタ後テスト	2026-08-03	下書き	本文	20260808115851	\N	20260808115851	\N	\N	\N
11	\N	\N	KN-011	最終確認エントリ	2026-08-03	下書き	本文	20260808115851	\N	20260808115851	\N	\N	\N
1	\N	\N	KN-001	賃上げ促進税制の適用要件まとめ	2026-08-04	公開中	賃上げ促進税制は、給与等支給額を前年度比で一定以上増加させた場合に法人税・所得税から税額控除を受けられる制度。中小企業の場合、雇用者全体の給与等支給額が1.5%以上増加した場合に控除率15%、2.5%以上増加した場合は控除率30%となる。教育訓練費を増加させた場合はさらに控除率が上乗せされる。適用には確定申告書等に控除額の計算に関する明細書の添付が必要。	20260808115851	\N	20260808115851	\N	\N	\N
14	\N	\N	KN-012	merge-test	2026-08-08	下書き	x	20260808125129	1	20260808125129	1	\N	\N
\.


--
-- Data for Name: trn_knowledge_entry_theme; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_knowledge_entry_theme (knowledge_entry_id, theme_id) FROM stdin;
1	13
5	13
2	14
4	14
7	14
4	15
7	16
8	16
3	18
6	19
\.


--
-- Data for Name: trn_kpi_monthly_stat; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_kpi_monthly_stat (kpi_monthly_stat_id, prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, year_month, support_count, ai_activity_count, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
2065	45	0021	2	\N	\N	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2066	00	0021	2	\N	\N	2025-09	4	0	20260812093232	\N	20260812093232	\N	\N	\N
2067	01	2020	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2068	04	2003	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2069	13	2001	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2070	46	2001	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2071	47	2001	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2072	01	0021	2	\N	2020	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2073	04	0021	2	\N	2003	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2074	13	0021	2	\N	2001	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2075	46	0021	2	\N	2001	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2076	47	0021	2	\N	2001	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2077	00	0021	2	01	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2078	00	0021	2	04	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2079	00	0021	2	13	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2080	00	0021	2	46	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2081	00	0021	2	47	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2082	01	0021	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2083	04	0021	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2084	13	0021	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2085	46	0021	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2086	47	0021	2	\N	\N	2025-10	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2087	00	0021	2	\N	\N	2025-10	10	0	20260812093232	\N	20260812093232	\N	\N	\N
2088	01	2010	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2089	36	2003	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2090	37	2001	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2091	46	2002	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2092	01	0021	2	\N	2010	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2093	36	0021	2	\N	2003	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2094	37	0021	2	\N	2001	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2095	46	0021	2	\N	2002	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2096	00	0021	2	01	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2097	00	0021	2	36	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2098	00	0021	2	37	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2099	00	0021	2	46	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2100	01	0021	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2101	36	0021	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2102	37	0021	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2103	46	0021	2	\N	\N	2025-11	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2104	00	0021	2	\N	\N	2025-11	8	0	20260812093232	\N	20260812093232	\N	\N	\N
2105	02	2001	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2106	08	2001	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2107	11	2001	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2108	14	2002	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2109	23	2001	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2110	36	2001	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2111	41	2001	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2112	46	2003	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2113	02	0021	2	\N	2001	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2114	08	0021	2	\N	2001	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2115	11	0021	2	\N	2001	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2116	14	0021	2	\N	2002	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2117	23	0021	2	\N	2001	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2118	36	0021	2	\N	2001	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2119	41	0021	2	\N	2001	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2120	46	0021	2	\N	2003	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2121	00	0021	2	02	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2122	00	0021	2	08	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2123	00	0021	2	11	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2124	00	0021	2	14	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2125	00	0021	2	23	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2126	00	0021	2	36	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2127	00	0021	2	41	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2128	00	0021	2	46	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2129	02	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2130	08	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2131	11	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2132	14	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2133	23	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2134	36	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2135	41	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2136	46	0021	2	\N	\N	2025-12	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2137	00	0021	2	\N	\N	2025-12	16	0	20260812093232	\N	20260812093232	\N	\N	\N
2138	01	2055	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2139	04	2002	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2140	22	2001	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2141	24	2002	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2142	26	2001	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2143	31	2002	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2144	34	2001	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2145	38	2001	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2146	43	2001	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2147	44	2001	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2148	01	0021	2	\N	2055	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2149	04	0021	2	\N	2002	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2150	22	0021	2	\N	2001	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2151	24	0021	2	\N	2002	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2152	26	0021	2	\N	2001	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2153	31	0021	2	\N	2002	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2154	34	0021	2	\N	2001	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2155	38	0021	2	\N	2001	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2156	43	0021	2	\N	2001	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2157	44	0021	2	\N	2001	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2158	00	0021	2	01	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2159	00	0021	2	04	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2160	00	0021	2	22	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2161	00	0021	2	24	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2162	00	0021	2	26	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2163	00	0021	2	31	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2164	00	0021	2	34	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2165	00	0021	2	38	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2166	00	0021	2	43	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2167	00	0021	2	44	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2168	01	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2169	04	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2170	22	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2171	24	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2172	26	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2173	31	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2174	34	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2175	38	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2176	43	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2177	44	0021	2	\N	\N	2026-01	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2178	00	0021	2	\N	\N	2026-01	20	0	20260812093232	\N	20260812093232	\N	\N	\N
2179	36	2003	2	\N	\N	2025-08	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2180	36	0021	2	\N	2003	2025-08	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2181	00	0021	2	36	\N	2025-08	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2182	36	0021	2	\N	\N	2025-08	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2183	00	0021	2	\N	\N	2025-08	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2184	01	2149	2	\N	\N	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2185	45	2001	2	\N	\N	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2186	01	0021	2	\N	2149	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2187	45	0021	2	\N	2001	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2188	00	0021	2	01	\N	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2189	00	0021	2	45	\N	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2190	01	0021	2	\N	\N	2025-09	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2191	01	2122	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2192	10	2001	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2193	19	2001	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2194	27	2001	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2195	30	2001	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2196	31	2001	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2197	41	2001	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2198	01	0021	3	\N	2122	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2199	10	0021	3	\N	2001	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2200	19	0021	3	\N	2001	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2201	27	0021	3	\N	2001	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2202	30	0021	3	\N	2001	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2203	31	0021	3	\N	2001	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2204	41	0021	3	\N	2001	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2205	00	0021	3	01	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2206	00	0021	3	10	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2207	00	0021	3	19	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2208	00	0021	3	27	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2209	00	0021	3	30	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2210	00	0021	3	31	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2211	00	0021	3	41	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2212	01	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2213	10	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2214	19	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2215	27	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2216	30	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2217	31	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2218	41	0021	3	\N	\N	2026-02	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2219	00	0021	3	\N	\N	2026-02	7	0	20260812093232	\N	20260812093232	\N	\N	\N
2220	01	2041	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2221	01	2149	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2222	03	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2223	08	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2224	15	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2225	21	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2226	24	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2227	24	2002	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2228	28	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2229	31	2001	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2230	01	0021	3	\N	2041	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2231	01	0021	3	\N	2149	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2232	03	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2233	08	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2234	15	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2235	21	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2236	24	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2237	24	0021	3	\N	2002	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2238	28	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2239	31	0021	3	\N	2001	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2240	00	0021	3	01	\N	2026-03	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2241	00	0021	3	03	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2242	00	0021	3	08	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2243	00	0021	3	15	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2244	00	0021	3	21	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2245	00	0021	3	24	\N	2026-03	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2246	00	0021	3	28	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2247	00	0021	3	31	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2248	01	0021	3	\N	\N	2026-03	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2249	03	0021	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2250	08	0021	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2251	15	0021	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2252	21	0021	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2253	24	0021	3	\N	\N	2026-03	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2254	28	0021	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2255	31	0021	3	\N	\N	2026-03	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2256	00	0021	3	\N	\N	2026-03	10	0	20260812093232	\N	20260812093232	\N	\N	\N
2257	01	2020	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2258	01	2055	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2259	01	2094	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2260	04	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2261	04	2002	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2262	05	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2263	08	2003	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2264	14	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2265	20	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2266	24	2003	3	\N	\N	2026-04	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2267	25	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2268	31	2003	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2269	36	2002	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2270	39	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2271	40	2001	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2272	01	0021	3	\N	2020	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2273	01	0021	3	\N	2055	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2274	01	0021	3	\N	2094	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2275	04	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2276	04	0021	3	\N	2002	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2277	05	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2278	08	0021	3	\N	2003	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2279	14	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2280	20	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2281	24	0021	3	\N	2003	2026-04	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2282	25	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2283	31	0021	3	\N	2003	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2284	36	0021	3	\N	2002	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2285	39	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2286	40	0021	3	\N	2001	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2287	00	0021	3	01	\N	2026-04	3	0	20260812093232	\N	20260812093232	\N	\N	\N
2288	00	0021	3	04	\N	2026-04	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2289	00	0021	3	05	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2290	00	0021	3	08	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2291	00	0021	3	14	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2292	00	0021	3	20	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2293	00	0021	3	24	\N	2026-04	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2294	00	0021	3	25	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2295	00	0021	3	31	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2296	00	0021	3	36	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2297	00	0021	3	39	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2298	00	0021	3	40	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2299	01	0021	3	\N	\N	2026-04	3	0	20260812093232	\N	20260812093232	\N	\N	\N
2300	04	0021	3	\N	\N	2026-04	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2301	05	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2302	08	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2303	14	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2304	20	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2305	24	0021	3	\N	\N	2026-04	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2306	25	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2307	31	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2308	36	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2309	39	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2310	40	0021	3	\N	\N	2026-04	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2311	00	0021	3	\N	\N	2026-04	16	0	20260812093232	\N	20260812093232	\N	\N	\N
2312	01	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2313	07	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2314	08	2002	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2315	12	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2316	13	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2317	14	2003	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2318	15	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2319	29	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2320	39	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2321	42	2001	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2322	01	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2323	07	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2324	08	0021	3	\N	2002	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2325	12	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2326	13	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2327	14	0021	3	\N	2003	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2328	15	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2329	29	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2330	39	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2331	42	0021	3	\N	2001	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2332	00	0021	3	01	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2333	00	0021	3	07	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2334	00	0021	3	08	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2335	00	0021	3	12	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2336	00	0021	3	13	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2337	00	0021	3	14	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2338	00	0021	3	15	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2339	00	0021	3	29	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2340	00	0021	3	39	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2341	00	0021	3	42	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2342	01	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2343	07	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2344	08	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2345	12	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2346	13	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2347	14	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2348	15	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2349	29	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2350	39	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2351	42	0021	3	\N	\N	2026-05	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2352	00	0021	3	\N	\N	2026-05	10	0	20260812093232	\N	20260812093232	\N	\N	\N
2353	01	2005	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2354	01	2020	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2355	06	2001	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2356	14	2002	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2357	14	2003	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2358	17	2001	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2359	18	2001	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2360	00	0021	3	36	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2361	01	0021	3	\N	\N	2026-06	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2362	06	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2363	14	0021	3	\N	\N	2026-06	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2364	17	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2365	18	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2366	25	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2367	32	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2368	35	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2369	36	0021	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2370	00	0021	3	\N	\N	2026-06	11	0	20260812093232	\N	20260812093232	\N	\N	\N
2371	01	2094	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2372	09	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2373	11	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2374	16	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2375	21	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2376	27	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2377	33	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2378	46	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2379	47	2001	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2380	01	0021	3	\N	2094	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2381	09	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2382	11	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2383	25	2001	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2384	32	2001	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2385	35	2001	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2386	36	2002	3	\N	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2387	01	0021	3	\N	2005	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2388	01	0021	3	\N	2020	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2389	06	0021	3	\N	2001	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2390	14	0021	3	\N	2002	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2391	14	0021	3	\N	2003	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2392	17	0021	3	\N	2001	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2393	18	0021	3	\N	2001	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2394	25	0021	3	\N	2001	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2395	32	0021	3	\N	2001	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2396	35	0021	3	\N	2001	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2397	36	0021	3	\N	2002	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2398	00	0021	3	01	\N	2026-06	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2399	00	0021	3	06	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2400	00	0021	3	14	\N	2026-06	2	0	20260812093232	\N	20260812093232	\N	\N	\N
2401	00	0021	3	17	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2402	00	0021	3	18	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2403	00	0021	3	25	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2404	00	0021	3	32	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2405	00	0021	3	35	\N	2026-06	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2406	16	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2407	21	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2408	27	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2409	33	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2410	46	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2411	47	0021	3	\N	2001	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2412	00	0021	3	01	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2413	00	0021	3	09	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2414	00	0021	3	11	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2415	00	0021	3	16	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2416	00	0021	3	21	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2417	00	0021	3	27	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2418	00	0021	3	33	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2419	00	0021	3	46	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2420	00	0021	3	47	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2421	01	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2422	09	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2423	11	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2424	16	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2425	21	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2426	27	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2427	33	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2428	46	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2429	47	0021	3	\N	\N	2026-07	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2430	00	0021	3	\N	\N	2026-07	9	0	20260812093232	\N	20260812093232	\N	\N	\N
2431	01	0021	3	\N	0021	2026-08	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2432	00	0021	3	01	\N	2026-08	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2433	01	0021	3	\N	\N	2026-08	1	0	20260812093232	\N	20260812093232	\N	\N	\N
2434	00	0021	3	\N	\N	2026-08	1	0	20260812093232	\N	20260812093232	\N	\N	\N
\.


--
-- Data for Name: trn_kpi_theme_breakdown; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_kpi_theme_breakdown (id, prefecture_code, shokokai_cd, fiscal_year_id, theme_id, support_count, year_month, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1047	41	2001	2	13	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1048	46	2003	2	20	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1049	02	0021	2	16	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1050	08	0021	2	17	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1051	11	0021	2	13	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1052	14	0021	2	14	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1053	23	0021	2	16	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1054	36	0021	2	18	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1055	41	0021	2	13	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1056	46	0021	2	20	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1057	00	0021	2	13	4	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1058	00	0021	2	14	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1059	00	0021	2	16	4	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1060	00	0021	2	17	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1061	00	0021	2	18	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1062	00	0021	2	20	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1063	01	2055	2	14	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1064	04	2002	2	18	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1065	22	2001	2	13	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1066	24	2002	2	15	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1067	26	2001	2	21	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1068	31	2002	2	13	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1069	34	2001	2	19	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1070	38	2001	2	18	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1071	43	2001	2	17	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1072	44	2001	2	17	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1073	01	0021	2	14	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1074	04	0021	2	18	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1075	22	0021	2	13	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1076	24	0021	2	15	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1077	26	0021	2	21	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1078	31	0021	2	13	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1079	34	0021	2	19	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1080	38	0021	2	18	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1081	43	0021	2	17	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1082	44	0021	2	17	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1083	00	0021	2	13	4	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1084	00	0021	2	14	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1085	00	0021	2	15	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1086	00	0021	2	17	4	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1087	00	0021	2	18	4	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1088	00	0021	2	19	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1089	00	0021	2	21	2	2026-01	20260812093232	\N	20260812093232	\N	\N	\N
1090	36	2003	2	20	2	2025-08	20260812093232	\N	20260812093232	\N	\N	\N
1091	36	0021	2	20	2	2025-08	20260812093232	\N	20260812093232	\N	\N	\N
1092	00	0021	2	20	2	2025-08	20260812093232	\N	20260812093232	\N	\N	\N
1093	01	2149	2	15	2	2025-09	20260812093232	\N	20260812093232	\N	\N	\N
1094	45	2001	2	16	2	2025-09	20260812093232	\N	20260812093232	\N	\N	\N
1095	01	0021	2	15	2	2025-09	20260812093232	\N	20260812093232	\N	\N	\N
1096	45	0021	2	16	2	2025-09	20260812093232	\N	20260812093232	\N	\N	\N
1097	00	0021	2	15	2	2025-09	20260812093232	\N	20260812093232	\N	\N	\N
1098	00	0021	2	16	2	2025-09	20260812093232	\N	20260812093232	\N	\N	\N
1099	01	2020	2	14	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1100	04	2003	2	17	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1101	13	2001	2	13	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1102	46	2001	2	20	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1103	47	2001	2	19	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1104	01	0021	2	14	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1105	04	0021	2	17	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1106	13	0021	2	13	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1107	46	0021	2	20	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1108	47	0021	2	19	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1109	00	0021	2	13	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1110	00	0021	2	14	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1111	00	0021	2	17	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1112	00	0021	2	19	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1113	00	0021	2	20	2	2025-10	20260812093232	\N	20260812093232	\N	\N	\N
1114	01	2010	2	20	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1115	36	2003	2	14	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1116	37	2001	2	15	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1117	46	2002	2	19	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1118	01	0021	2	20	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1119	36	0021	2	14	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1120	37	0021	2	15	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1121	46	0021	2	19	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1122	00	0021	2	14	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1123	00	0021	2	15	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1124	00	0021	2	19	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1125	00	0021	2	20	2	2025-11	20260812093232	\N	20260812093232	\N	\N	\N
1126	02	2001	2	16	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1127	08	2001	2	17	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1128	11	2001	2	13	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1129	14	2002	2	14	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1130	23	2001	2	16	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1131	36	2001	2	18	2	2025-12	20260812093232	\N	20260812093232	\N	\N	\N
1132	01	2122	3	18	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1133	10	2001	3	19	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1134	19	2001	3	17	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1135	27	2001	3	16	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1136	30	2001	3	16	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1137	31	2001	3	15	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1138	41	2001	3	13	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1139	01	0021	3	18	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1140	10	0021	3	19	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1141	19	0021	3	17	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1142	27	0021	3	16	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1143	30	0021	3	16	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1144	31	0021	3	15	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1145	41	0021	3	13	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1146	00	0021	3	13	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1147	00	0021	3	15	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1148	00	0021	3	16	2	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1149	00	0021	3	17	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1150	00	0021	3	18	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1151	00	0021	3	19	1	2026-02	20260812093232	\N	20260812093232	\N	\N	\N
1152	01	2041	3	18	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1153	01	2149	3	14	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1154	03	2001	3	21	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1155	08	2001	3	19	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1156	15	2001	3	16	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1157	21	2001	3	19	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1158	24	2001	3	17	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1159	24	2002	3	15	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1160	28	2001	3	19	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1161	31	2001	3	18	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1162	01	0021	3	14	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1163	01	0021	3	18	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1164	03	0021	3	21	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1165	08	0021	3	19	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1166	15	0021	3	16	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1167	21	0021	3	19	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1168	24	0021	3	15	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1169	24	0021	3	17	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1170	28	0021	3	19	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1171	31	0021	3	18	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1172	00	0021	3	14	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1173	00	0021	3	15	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1174	00	0021	3	16	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1175	00	0021	3	17	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1176	00	0021	3	18	2	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1177	00	0021	3	19	3	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1178	00	0021	3	21	1	2026-03	20260812093232	\N	20260812093232	\N	\N	\N
1179	01	2020	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1180	01	2055	3	21	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1181	01	2094	3	14	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1182	04	2001	3	21	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1183	04	2002	3	20	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1184	05	2001	3	20	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1185	08	2003	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1186	14	2001	3	20	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1187	20	2001	3	18	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1188	24	2003	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1189	24	2003	3	19	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1190	25	2001	3	14	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1191	31	2003	3	17	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1192	36	2002	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1193	39	2001	3	17	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1194	40	2001	3	19	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1195	01	0021	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1196	01	0021	3	14	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1197	01	0021	3	21	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1198	04	0021	3	20	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1199	04	0021	3	21	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1200	05	0021	3	20	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1201	08	0021	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1202	14	0021	3	20	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1203	20	0021	3	18	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1204	24	0021	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1205	24	0021	3	19	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1206	25	0021	3	14	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1207	31	0021	3	17	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1208	36	0021	3	13	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1209	39	0021	3	17	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1210	40	0021	3	19	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1211	00	0021	3	13	4	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1212	00	0021	3	14	2	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1213	00	0021	3	17	2	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1214	00	0021	3	18	1	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1215	00	0021	3	19	2	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1216	00	0021	3	20	3	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1217	00	0021	3	21	2	2026-04	20260812093232	\N	20260812093232	\N	\N	\N
1218	01	2001	3	19	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1219	07	2001	3	15	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1220	08	2002	3	21	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1221	12	2001	3	21	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1222	13	2001	3	16	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1223	14	2003	3	19	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1224	15	2001	3	13	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1225	29	2001	3	20	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1226	39	2001	3	20	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1227	42	2001	3	15	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1228	01	0021	3	19	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1229	07	0021	3	15	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1230	08	0021	3	21	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1231	12	0021	3	21	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1232	13	0021	3	16	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1233	14	0021	3	19	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1234	15	0021	3	13	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1235	29	0021	3	20	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1236	39	0021	3	20	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1237	42	0021	3	15	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1238	00	0021	3	13	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1239	00	0021	3	15	2	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1240	00	0021	3	16	1	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1241	00	0021	3	19	2	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1242	00	0021	3	20	2	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1243	00	0021	3	21	2	2026-05	20260812093232	\N	20260812093232	\N	\N	\N
1244	01	2005	3	18	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1245	01	2020	3	16	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1246	06	2001	3	13	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1247	14	2002	3	13	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1248	14	2003	3	21	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1249	17	2001	3	16	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1250	18	2001	3	16	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1251	25	2001	3	20	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1252	32	2001	3	21	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1253	35	2001	3	21	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1254	36	2002	3	17	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1255	01	0021	3	16	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1256	01	0021	3	18	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1257	06	0021	3	13	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1258	14	0021	3	13	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1259	14	0021	3	21	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1260	17	0021	3	16	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1261	18	0021	3	16	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1262	25	0021	3	20	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1263	32	0021	3	21	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1264	35	0021	3	21	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1265	36	0021	3	17	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1266	00	0021	3	13	2	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1267	00	0021	3	16	3	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1268	00	0021	3	17	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1269	00	0021	3	18	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1270	00	0021	3	20	1	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1271	00	0021	3	21	3	2026-06	20260812093232	\N	20260812093232	\N	\N	\N
1272	01	2094	3	20	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1273	09	2001	3	21	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1274	11	2001	3	13	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1275	16	2001	3	15	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1276	21	2001	3	20	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1277	27	2001	3	17	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1278	33	2001	3	15	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1279	46	2001	3	14	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1280	47	2001	3	13	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1281	01	0021	3	20	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1282	09	0021	3	21	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1283	01	0021	3	13	1	2026-08	20260812093232	\N	20260812093232	\N	\N	\N
1284	00	0021	3	13	1	2026-08	20260812093232	\N	20260812093232	\N	\N	\N
1285	11	0021	3	13	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1286	16	0021	3	15	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1287	21	0021	3	20	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1288	27	0021	3	17	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1289	33	0021	3	15	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1290	46	0021	3	14	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1291	47	0021	3	13	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1292	00	0021	3	13	2	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1293	00	0021	3	14	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1294	00	0021	3	15	2	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1295	00	0021	3	17	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1296	00	0021	3	20	2	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
1297	00	0021	3	21	1	2026-07	20260812093232	\N	20260812093232	\N	\N	\N
\.


--
-- Data for Name: trn_notice; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_notice (notice_id, notice_code, role_code, content, start_date, end_date, sort_order, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
5	no-shk-001	shokokai	令和8年度7月分の報告書提出期限は8/15です	2026-07-15	2027-03-31	0	20260808115851	\N	20260808115851	\N	\N	\N
6	no-shk-002	shokokai	下書きの報告書があります、確認してください	2026-07-01	2026-07-31	1	20260808115851	\N	20260808115851	\N	\N	\N
7	login-001	login	定期メンテナンスのお知らせ：8/10(月) 2:00〜5:00はシステムをご利用いただけません	2026-07-25	2026-08-10	0	20260808115851	\N	20260808115851	\N	\N	\N
8	login-002	login	「AI支援提案」機能を追加しました。ぜひご活用ください	2026-07-01	2026-08-31	1	20260808115851	\N	20260808115851	\N	\N	\N
1	no-nat-001	zenkoku	令和8年度7月分の報告書提出期限は8/15です	2026-07-15	2027-03-31	0	20260808115851	\N	20260808115851	\N	\N	\N
2	no-nat-002	zenkoku	様式I 提出期限延長のお知らせを全県連へ送信しました（期限 8/5）	2026-07-20	2026-08-05	1	20260808115851	\N	20260808115851	\N	\N	\N
3	no-pref-001	ken	令和8年度7月分の報告書提出期限は8/15です	2026-07-15	2027-03-31	0	20260808115851	\N	20260808115851	\N	\N	\N
4	no-pref-002	ken	全国連より：月次報告 様式I 提出期限延長のお知らせ（期限 8/5）	2026-07-20	2026-08-05	1	20260808115851	\N	20260808115851	\N	\N	\N
\.


--
-- Data for Name: trn_report; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_report (report_id, report_code, form_code, fiscal_year_id, prefecture_code, shokokai_cd, theme_id, industry_code, capital_range_id, employee_range_id, revenue_range_id, expert_qualification_id, visit_result_id, report_date, summary, content, voice_transcript, time_start, time_end, business_person, business_name, staff_main_name, staff_sub_name, attendee_count, expert_name, location, current_issue, support_content, support_result, venue_name, registered_at, status, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by, printed_at) FROM stdin;
212	RPT-0095	G-2	3	01	0021	14	C	\N	\N	\N	\N	\N	2026-08-12	概要	内容	\N	14:58	15:00	担当者	事業所	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-12	登録済み	20260812145825	90	20260812145825	90	\N	\N	\N
211	RPT-0094	G-7	3	01	0021	13	R	\N	\N	\N	\N	2	2026-08-09	内容	内容	\N	11:07	14:10	担当者	事業所	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-09	登録済み	20260809100652	90	20260813092541	90	\N	\N	\N
118	RPT-0001	G-2	3	01	2001	19	N	\N	\N	\N	\N	\N	2026-05-12	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	13:30	14:00	鈴木 隆	新町食堂	田中 一郎	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-13	登録済み	20260809010938	\N	20260809010938	\N	\N	\N	\N
119	RPT-0002	F	3	01	2005	18	F	\N	\N	\N	\N	\N	2026-06-13	2割特例適用の相談	2割特例の適用可否について相談を受け、税理士への相談を案内した。	\N	10:30	11:30	田中 美咲	新町製作所	鈴木 次郎	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-16	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
120	RPT-0003	G-6	3	01	2010	20	B	\N	\N	\N	\N	\N	2025-11-09	事業再構築の相談	事業再構築による新分野展開について相談を受け、補助金の申請支援を行った。	\N	16:30	17:15	田中 太郎	山田食堂	佐藤 三郎	\N	\N	\N	\N	\N	\N	\N	\N	2025-11-09	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
121	RPT-0004	G-3	3	01	2020	14	M	\N	\N	\N	\N	\N	2025-10-10	業務フロー見直し相談	業務フローの見直しと外部委託の活用について相談を受け、専門家派遣による業務改善支援につなげた。	\N	10:00	11:00	中村 美咲	友和工業	高橋 久美子	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-12	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
122	RPT-0005	G-4	3	01	2020	13	R	\N	\N	\N	\N	\N	2026-04-27	価格転嫁の進め方相談	最低賃金引上げに対応した価格転嫁の進め方について、取引先との交渉方法を含めて助言した。	\N	09:00	10:30	小林 直樹	さくらクリニック	テスト太郎2	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-27	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
123	RPT-0006	G-4	3	01	2020	16	I	\N	\N	\N	\N	\N	2026-06-10	クラウド会計導入相談	会計業務のクラウド化について相談があり、IT導入補助金の申請支援を行った。	\N	11:00	12:30	渡辺 亜紀	さくら製作所	テスト太郎2	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-11	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
124	RPT-0007	G-8	3	01	2041	18	E	\N	\N	\N	\N	\N	2026-03-17	経理体制整備の相談	インボイス制度対応の経理体制整備について相談を受け、会計ソフト導入補助金を案内した。	\N	15:00	15:30	佐藤 太郎	ひまわりカフェ	伊藤 和也	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-19	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
125	RPT-0008	G-7	3	01	2055	21	K	\N	\N	\N	\N	\N	2026-04-16	補助金申請書類整理の相談	補助金申請に必要な書類の整理について相談があり、提出書類のチェックリストを案内した。	\N	16:00	17:30	鈴木 健一	本町運送	渡辺 隆	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-17	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
126	RPT-0009	G-5	3	01	2055	14	A	\N	\N	\N	\N	\N	2026-01-18	省力化補助金の活用相談	人手不足による受注機会の損失について相談があり、省力化補助金を活用した設備導入を提案した。	\N	14:00	14:30	渡辺 誠	さくら製作所	渡辺 隆	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-18	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
127	RPT-0010	G-7	3	01	2094	14	O	\N	\N	\N	\N	\N	2026-04-25	多能工化の相談	人材確保が困難な状況について相談があり、多能工化や兼務体制の整備を提案した。	\N	10:30	11:00	伊藤 亜紀	つばき商店	山本 恵美	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-27	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
128	RPT-0011	G-2	3	01	2094	20	Q	\N	\N	\N	\N	\N	2026-07-01	事業再構築の相談	事業再構築による新分野展開について相談を受け、補助金の申請支援を行った。	\N	10:30	11:00	田中 亜紀	さくらカフェ	山本 恵美	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-02	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
129	RPT-0012	G-5	3	01	2122	18	A	\N	\N	\N	\N	\N	2026-02-03	2割特例適用の相談	2割特例の適用可否について相談を受け、税理士への相談を案内した。	\N	11:30	12:30	中村 恵子	つばき不動産	中村 誠	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-04	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
130	RPT-0013	G-3	3	01	2149	15	Q	\N	\N	\N	\N	\N	2025-09-29	省エネ設備導入相談	燃料費・電気代の高騰による収益悪化について相談を受け、省エネ設備導入補助金の活用を案内した。	\N	13:00	14:00	渡辺 健一	共栄美容室	加藤 由美	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-01	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
131	RPT-0014	G-6	3	01	2149	14	S	\N	\N	\N	\N	\N	2026-03-08	多能工化の相談	人材確保が困難な状況について相談があり、多能工化や兼務体制の整備を提案した。	\N	11:00	11:30	佐藤 太郎	さくら運送	加藤 由美	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-08	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
132	RPT-0015	G-2	3	02	2001	16	I	\N	\N	\N	\N	\N	2025-12-06	ECサイト構築相談	ECサイト構築による販路拡大について相談を受け、小規模事業者持続化補助金（デジタル枠）の活用を案内した。	\N	11:30	12:15	小林 誠	第一工業	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-07	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
133	RPT-0016	F	3	03	2001	21	C	\N	\N	\N	\N	\N	2026-03-08	月次報告書作成の相談	月次報告書の作成方法について相談を受け、様式の記入方法を説明した。	\N	13:30	15:00	渡辺 健一	ひまわり建設	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-10	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
134	RPT-0017	G-8	3	04	2001	21	B	\N	\N	\N	\N	\N	2026-04-15	月次報告書作成の相談	月次報告書の作成方法について相談を受け、様式の記入方法を説明した。	\N	15:00	16:30	中村 由美	さくら食堂	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-18	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
135	RPT-0018	F	3	04	2002	18	T	\N	\N	\N	\N	\N	2026-01-15	経理体制整備の相談	インボイス制度対応の経理体制整備について相談を受け、会計ソフト導入補助金を案内した。	\N	11:00	11:30	小林 隆	松風カフェ	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-15	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
136	RPT-0019	G-6	3	04	2002	20	J	\N	\N	\N	\N	\N	2026-04-30	コロナ融資返済相談	コロナ関連融資の返済条件見直しについて相談を受け、伴走支援型特別保証制度を案内した。	\N	09:00	09:45	中村 花子	みどり製作所	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-30	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
137	RPT-0020	G-7	3	04	2003	17	S	\N	\N	\N	\N	\N	2025-10-13	輸出先多角化の相談	米国向け輸出における関税負担増加について相談を受け、輸出先の多角化に向けた海外展示会出展を案内した。	\N	16:30	17:00	加藤 美咲	共栄商店	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-13	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
138	RPT-0021	G-4	3	05	2001	20	F	\N	\N	\N	\N	\N	2026-04-17	事業再構築の相談	事業再構築による新分野展開について相談を受け、補助金の申請支援を行った。	\N	11:00	12:30	渡辺 美咲	新町美容室	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-19	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
139	RPT-0022	G-7	3	06	2001	13	I	\N	\N	\N	\N	\N	2026-06-05	最低賃金引上げへの対応相談	最低賃金引上げに伴う人件費増加への対応について相談を受けた。業務改善助成金の活用を提案し、設備投資による生産性向上を通じた賃上げ原資の確保を支援した。	\N	10:00	11:30	小林 花子	つばきクリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-07	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
140	RPT-0023	G-6	3	07	2001	15	E	\N	\N	\N	\N	\N	2026-05-26	価格転嫁交渉の相談	原材料価格の上昇に伴う価格転嫁について相談があり、取引先との交渉のポイントを助言した。	\N	13:00	14:30	伊藤 隆	山田クリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-27	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
141	RPT-0024	G-4	3	08	2001	17	F	\N	\N	\N	\N	\N	2025-12-11	輸出先多角化の相談	米国向け輸出における関税負担増加について相談を受け、輸出先の多角化に向けた海外展示会出展を案内した。	\N	11:00	11:30	田中 由美	本町運送	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-12	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
142	RPT-0025	F	3	08	2001	19	L	\N	\N	\N	\N	\N	2026-03-13	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	13:30	14:30	伊藤 直樹	山田建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-15	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
143	RPT-0026	G-5	3	08	2002	21	T	\N	\N	\N	\N	\N	2026-05-30	補助金申請書類整理の相談	補助金申請に必要な書類の整理について相談があり、提出書類のチェックリストを案内した。	\N	16:30	18:00	佐藤 隆	みどり運送	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-02	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
144	RPT-0027	G-7	3	08	2003	13	T	\N	\N	\N	\N	\N	2026-04-01	価格転嫁の進め方相談	最低賃金引上げに対応した価格転嫁の進め方について、取引先との交渉方法を含めて助言した。	\N	10:30	11:00	鈴木 隆	共栄美容室	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-04	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
145	RPT-0028	G-6	3	09	2001	21	G	\N	\N	\N	\N	\N	2026-07-13	月次報告書作成の相談	月次報告書の作成方法について相談を受け、様式の記入方法を説明した。	\N	15:30	17:00	中村 恵子	さくら商店	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-14	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
146	RPT-0029	F	3	10	2001	19	B	\N	\N	\N	\N	\N	2026-02-24	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	14:30	15:00	鈴木 由美	ひまわりクリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-26	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
147	RPT-0030	G-3	3	11	2001	13	N	\N	\N	\N	\N	\N	2026-07-28	最低賃金引上げへの対応相談	最低賃金引上げに伴う人件費増加への対応について相談を受けた。業務改善助成金の活用を提案し、設備投資による生産性向上を通じた賃上げ原資の確保を支援した。	\N	15:00	15:30	中村 隆	新町カフェ	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-31	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
148	RPT-0031	G-8	3	11	2001	13	T	\N	\N	\N	\N	\N	2025-12-14	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	14:30	16:00	高橋 亜紀	つばきカフェ	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-17	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
149	RPT-0032	G-5	3	12	2001	21	N	\N	\N	\N	\N	\N	2026-05-09	月次報告書作成の相談	月次報告書の作成方法について相談を受け、様式の記入方法を説明した。	\N	11:00	12:30	渡辺 直樹	ひまわり工業	■■商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-10	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
150	RPT-0033	G-3	3	13	2001	13	O	\N	\N	\N	\N	\N	2025-10-11	価格転嫁の進め方相談	最低賃金引上げに対応した価格転嫁の進め方について、取引先との交渉方法を含めて助言した。	\N	16:30	17:30	小林 健一	中央製作所	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-14	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
151	RPT-0034	G-7	3	13	2001	16	A	\N	\N	\N	\N	\N	2026-05-23	ECサイト構築相談	ECサイト構築による販路拡大について相談を受け、小規模事業者持続化補助金（デジタル枠）の活用を案内した。	\N	15:30	16:00	渡辺 健一	中央美容室	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-25	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
152	RPT-0035	G-5	3	14	2001	20	H	\N	\N	\N	\N	\N	2026-04-09	新商品開発の相談	コロナ後の需要変化に対応した新商品開発について相談があり、持続化補助金の活用を提案した。	\N	11:00	11:45	鈴木 由美	あおば工業	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-10	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
153	RPT-0036	G-8	3	14	2002	14	C	\N	\N	\N	\N	\N	2025-12-10	省力化補助金の活用相談	人手不足による受注機会の損失について相談があり、省力化補助金を活用した設備導入を提案した。	\N	11:30	13:00	鈴木 恵子	さくら運送	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-12	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
154	RPT-0037	G-7	3	14	2002	13	Q	\N	\N	\N	\N	\N	2026-06-13	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	11:30	12:15	伊藤 隆	白鳥食堂	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-14	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
155	RPT-0038	G-2	3	14	2003	19	P	\N	\N	\N	\N	\N	2026-05-24	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	13:30	14:15	田中 亜紀	本町建設	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-24	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
156	RPT-0039	G-5	3	14	2003	21	A	\N	\N	\N	\N	\N	2026-06-09	実績報告準備の相談	事業実施計画の進捗管理について相談を受け、実績報告の準備を支援した。	\N	09:00	09:45	鈴木 誠	本町運送	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-11	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
157	RPT-0040	G-3	3	15	2001	16	N	\N	\N	\N	\N	\N	2026-03-02	ECサイト構築相談	ECサイト構築による販路拡大について相談を受け、小規模事業者持続化補助金（デジタル枠）の活用を案内した。	\N	14:00	14:30	加藤 太郎	白鳥クリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-04	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
158	RPT-0041	G-8	3	15	2001	13	K	\N	\N	\N	\N	\N	2026-05-18	最低賃金引上げへの対応相談	最低賃金引上げに伴う人件費増加への対応について相談を受けた。業務改善助成金の活用を提案し、設備投資による生産性向上を通じた賃上げ原資の確保を支援した。	\N	13:00	14:00	伊藤 健一	中央不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-19	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
159	RPT-0042	G-3	3	16	2001	15	F	\N	\N	\N	\N	\N	2026-07-08	省エネ設備導入相談	燃料費・電気代の高騰による収益悪化について相談を受け、省エネ設備導入補助金の活用を案内した。	\N	09:30	10:30	加藤 由美	つばきカフェ	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-11	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
160	RPT-0043	F	3	17	2001	16	B	\N	\N	\N	\N	\N	2026-06-11	キャッシュレス導入相談	キャッシュレス決済の導入について相談を受け、導入費用の補助制度を案内した。	\N	14:00	14:30	佐藤 由美	あおば工業	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-12	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
161	RPT-0044	G-3	3	18	2001	16	L	\N	\N	\N	\N	\N	2026-06-23	キャッシュレス導入相談	キャッシュレス決済の導入について相談を受け、導入費用の補助制度を案内した。	\N	14:00	14:30	伊藤 太郎	第一クリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-25	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
162	RPT-0045	G-7	3	19	2001	17	J	\N	\N	\N	\N	\N	2026-02-11	関税影響試算の相談	関税影響のシミュレーションについて相談があり、採算への影響を試算のうえ価格戦略の見直しを助言した。	\N	15:30	17:00	小林 誠	中央食堂	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-13	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
164	RPT-0047	F	3	21	2001	19	M	\N	\N	\N	\N	\N	2026-03-06	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	16:00	16:30	佐藤 健一	ひまわり不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-09	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
165	RPT-0048	G-6	3	21	2001	20	E	\N	\N	\N	\N	\N	2026-07-18	新商品開発の相談	コロナ後の需要変化に対応した新商品開発について相談があり、持続化補助金の活用を提案した。	\N	09:00	09:30	中村 由美	白鳥不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-19	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
166	RPT-0049	G-4	3	22	2001	13	O	\N	\N	\N	\N	\N	2026-01-11	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	13:00	14:00	佐藤 花子	第一不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-11	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
167	RPT-0050	F	3	23	2001	16	J	\N	\N	\N	\N	\N	2025-12-23	キャッシュレス導入相談	キャッシュレス決済の導入について相談を受け、導入費用の補助制度を案内した。	\N	13:30	14:30	渡辺 花子	green工業	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-23	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
168	RPT-0051	G-4	3	24	2001	17	S	\N	\N	\N	\N	\N	2026-03-16	輸出先多角化の相談	米国向け輸出における関税負担増加について相談を受け、輸出先の多角化に向けた海外展示会出展を案内した。	\N	16:00	17:30	中村 恵子	松風クリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-16	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
169	RPT-0052	G-4	3	24	2002	15	A	\N	\N	\N	\N	\N	2026-03-26	省エネ設備導入相談	燃料費・電気代の高騰による収益悪化について相談を受け、省エネ設備導入補助金の活用を案内した。	\N	10:00	11:00	加藤 健一	中央クリニック	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-27	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
170	RPT-0053	G-6	3	24	2002	15	F	\N	\N	\N	\N	\N	2026-01-14	価格転嫁交渉の相談	原材料価格の上昇に伴う価格転嫁について相談があり、取引先との交渉のポイントを助言した。	\N	10:30	12:00	高橋 隆	共栄製作所	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-14	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
171	RPT-0054	G-2	3	24	2003	19	F	\N	\N	\N	\N	\N	2026-04-20	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	15:30	16:30	田中 誠	新町不動産	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-21	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
172	RPT-0055	G-5	3	24	2003	13	E	\N	\N	\N	\N	\N	2026-04-12	価格転嫁の進め方相談	最低賃金引上げに対応した価格転嫁の進め方について、取引先との交渉方法を含めて助言した。	\N	09:30	10:15	伊藤 誠	友和製作所	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-12	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
173	RPT-0056	G-8	3	25	2001	20	L	\N	\N	\N	\N	\N	2026-06-13	コロナ融資返済相談	コロナ関連融資の返済条件見直しについて相談を受け、伴走支援型特別保証制度を案内した。	\N	09:00	09:30	渡辺 誠	ひまわりクリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-16	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
174	RPT-0057	G-7	3	25	2001	14	K	\N	\N	\N	\N	\N	2026-04-12	業務フロー見直し相談	業務フローの見直しと外部委託の活用について相談を受け、専門家派遣による業務改善支援につなげた。	\N	15:30	17:00	中村 誠	共栄不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-15	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
175	RPT-0058	G-3	3	26	2001	21	T	\N	\N	\N	\N	\N	2026-01-01	実績報告準備の相談	事業実施計画の進捗管理について相談を受け、実績報告の準備を支援した。	\N	16:30	17:30	高橋 恵子	中央商店	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-03	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
176	RPT-0059	G-2	3	27	2001	16	E	\N	\N	\N	\N	\N	2026-02-20	クラウド会計導入相談	会計業務のクラウド化について相談があり、IT導入補助金の申請支援を行った。	\N	09:00	10:30	佐藤 亜紀	共栄商店	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-20	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
177	RPT-0060	G-2	3	27	2001	17	P	\N	\N	\N	\N	\N	2026-07-19	輸出先多角化の相談	米国向け輸出における関税負担増加について相談を受け、輸出先の多角化に向けた海外展示会出展を案内した。	\N	16:30	17:00	伊藤 亜紀	本町クリニック	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-20	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
178	RPT-0061	G-4	3	28	2001	19	A	\N	\N	\N	\N	\N	2026-03-04	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	09:00	09:45	小林 美咲	白鳥工業	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-06	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
179	RPT-0062	G-5	3	29	2001	20	R	\N	\N	\N	\N	\N	2026-05-23	事業再構築の相談	事業再構築による新分野展開について相談を受け、補助金の申請支援を行った。	\N	14:00	15:30	加藤 花子	友和商店	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-25	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
180	RPT-0063	G-2	3	30	2001	16	C	\N	\N	\N	\N	\N	2026-02-21	クラウド会計導入相談	会計業務のクラウド化について相談があり、IT導入補助金の申請支援を行った。	\N	09:30	11:00	伊藤 亜紀	友和クリニック	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-22	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
181	RPT-0064	G-2	3	31	2001	15	O	\N	\N	\N	\N	\N	2026-02-11	省エネ設備導入相談	燃料費・電気代の高騰による収益悪化について相談を受け、省エネ設備導入補助金の活用を案内した。	\N	13:00	13:30	小林 恵子	あおば食堂	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-14	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
182	RPT-0065	F	3	31	2001	18	A	\N	\N	\N	\N	\N	2026-03-08	免税事業者取引の相談	免税事業者との取引条件について相談があり、下請取引の留意点を助言した。	\N	10:00	10:45	高橋 太郎	新町工業	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-03-08	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
183	RPT-0066	G-4	3	31	2002	13	O	\N	\N	\N	\N	\N	2026-01-03	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	10:30	11:15	加藤 花子	ひまわり食堂	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-05	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
184	RPT-0067	G-4	3	31	2003	17	I	\N	\N	\N	\N	\N	2026-04-04	関税影響試算の相談	関税影響のシミュレーションについて相談があり、採算への影響を試算のうえ価格戦略の見直しを助言した。	\N	16:30	17:00	鈴木 花子	友和運送	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-04	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
185	RPT-0068	G-6	3	32	2001	21	F	\N	\N	\N	\N	\N	2026-06-03	実績報告準備の相談	事業実施計画の進捗管理について相談を受け、実績報告の準備を支援した。	\N	13:30	14:30	中村 恵子	ひまわり商店	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-05	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
186	RPT-0069	G-6	3	33	2001	15	N	\N	\N	\N	\N	\N	2026-07-18	省エネ設備導入相談	燃料費・電気代の高騰による収益悪化について相談を受け、省エネ設備導入補助金の活用を案内した。	\N	10:00	10:30	佐藤 花子	みどり不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-19	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
187	RPT-0070	G-4	3	34	2001	19	E	\N	\N	\N	\N	\N	2026-01-31	タイムスタンプ要件の相談	会計システムのタイムスタンプ要件対応について相談を受け、システム更新の検討を案内した。	\N	14:00	15:00	加藤 美咲	さくらカフェ	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-31	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
188	RPT-0071	G-7	3	35	2001	21	J	\N	\N	\N	\N	\N	2026-06-19	実績報告準備の相談	事業実施計画の進捗管理について相談を受け、実績報告の準備を支援した。	\N	15:30	16:15	佐藤 由美	松風不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-21	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
189	RPT-0072	G-7	3	36	2001	18	E	\N	\N	\N	\N	\N	2025-12-24	免税事業者取引の相談	免税事業者との取引条件について相談があり、下請取引の留意点を助言した。	\N	11:00	11:30	佐藤 亜紀	松風食堂	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-24	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
190	RPT-0073	F	3	36	2002	17	C	\N	\N	\N	\N	\N	2026-06-28	価格交渉の相談	取引先との価格交渉について相談を受け、コスト増加分の転嫁方法を助言した。	\N	16:30	17:30	鈴木 誠	白鳥運送	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-30	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
191	RPT-0074	F	3	36	2002	13	B	\N	\N	\N	\N	\N	2026-04-25	最低賃金引上げへの対応相談	最低賃金引上げに伴う人件費増加への対応について相談を受けた。業務改善助成金の活用を提案し、設備投資による生産性向上を通じた賃上げ原資の確保を支援した。	\N	14:00	14:45	高橋 花子	中央製作所	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-27	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
192	RPT-0075	G-3	3	36	2003	20	R	\N	\N	\N	\N	\N	2025-08-18	コロナ融資返済相談	コロナ関連融資の返済条件見直しについて相談を受け、伴走支援型特別保証制度を案内した。	\N	15:30	16:30	鈴木 亜紀	白鳥工業	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-08-21	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
193	RPT-0076	G-6	3	36	2003	14	P	\N	\N	\N	\N	\N	2025-11-24	省力化補助金の活用相談	人手不足による受注機会の損失について相談があり、省力化補助金を活用した設備導入を提案した。	\N	16:30	18:00	佐藤 直樹	中央食堂	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-11-26	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
194	RPT-0077	G-4	3	37	2001	15	O	\N	\N	\N	\N	\N	2025-11-16	電力契約見直し相談	電力契約の見直しによるコスト削減について相談を受け、複数年契約プランの比較検討を支援した。	\N	10:00	10:45	高橋 由美	さくら運送	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-11-18	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
195	RPT-0078	G-2	3	38	2001	18	R	\N	\N	\N	\N	\N	2026-01-09	経理体制整備の相談	インボイス制度対応の経理体制整備について相談を受け、会計ソフト導入補助金を案内した。	\N	10:00	10:45	中村 恵子	山田建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-09	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
196	RPT-0079	G-2	3	39	2001	17	R	\N	\N	\N	\N	\N	2026-04-23	関税影響試算の相談	関税影響のシミュレーションについて相談があり、採算への影響を試算のうえ価格戦略の見直しを助言した。	\N	10:30	12:00	小林 恵子	ひまわり商店	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-24	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
197	RPT-0080	G-6	3	39	2001	20	M	\N	\N	\N	\N	\N	2026-05-22	コロナ融資返済相談	コロナ関連融資の返済条件見直しについて相談を受け、伴走支援型特別保証制度を案内した。	\N	11:30	12:00	山本 誠	みどり商店	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-23	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
198	RPT-0081	G-5	3	40	2001	19	T	\N	\N	\N	\N	\N	2026-04-22	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	09:00	10:30	山本 恵子	第一商店	■■商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-24	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
199	RPT-0082	G-4	3	41	2001	13	T	\N	\N	\N	\N	\N	2025-12-29	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	15:00	16:30	田中 花子	共栄工業	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-29	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
200	RPT-0083	F	3	41	2001	13	Q	\N	\N	\N	\N	\N	2026-02-18	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	15:30	16:00	渡辺 恵子	みどり運送	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-02-20	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
201	RPT-0084	G-8	3	42	2001	15	Q	\N	\N	\N	\N	\N	2026-05-17	価格転嫁交渉の相談	原材料価格の上昇に伴う価格転嫁について相談があり、取引先との交渉のポイントを助言した。	\N	14:00	15:00	中村 健一	第一不動産	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-05-19	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
202	RPT-0085	G-4	3	43	2001	17	Q	\N	\N	\N	\N	\N	2026-01-12	関税影響試算の相談	関税影響のシミュレーションについて相談があり、採算への影響を試算のうえ価格戦略の見直しを助言した。	\N	15:00	15:30	小林 恵子	さくら建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-13	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
203	RPT-0086	G-2	3	44	2001	17	S	\N	\N	\N	\N	\N	2026-01-12	輸出先多角化の相談	米国向け輸出における関税負担増加について相談を受け、輸出先の多角化に向けた海外展示会出展を案内した。	\N	11:30	13:00	中村 恵子	みどり建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-01-14	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
204	RPT-0087	G-7	3	45	2001	16	T	\N	\N	\N	\N	\N	2025-09-05	キャッシュレス導入相談	キャッシュレス決済の導入について相談を受け、導入費用の補助制度を案内した。	\N	15:00	16:30	小林 美咲	あおば建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-09-06	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
205	RPT-0088	G-8	3	46	2001	20	I	\N	\N	\N	\N	\N	2025-10-15	新商品開発の相談	コロナ後の需要変化に対応した新商品開発について相談があり、持続化補助金の活用を提案した。	\N	13:00	14:00	鈴木 恵子	あおば工業	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-16	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
206	RPT-0089	G-2	3	46	2001	14	L	\N	\N	\N	\N	\N	2026-07-20	省力化補助金の活用相談	人手不足による受注機会の損失について相談があり、省力化補助金を活用した設備導入を提案した。	\N	13:30	14:15	加藤 誠	ひまわり建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-23	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
207	RPT-0090	G-8	3	46	2002	19	K	\N	\N	\N	\N	\N	2025-11-03	スキャナ保存の相談	スキャナ保存制度の活用について相談があり、運用フローの見直しを助言した。	\N	13:30	14:15	中村 誠	松風運送	△△商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-11-06	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
208	RPT-0091	G-5	3	46	2003	20	C	\N	\N	\N	\N	\N	2025-12-23	新商品開発の相談	コロナ後の需要変化に対応した新商品開発について相談があり、持続化補助金の活用を提案した。	\N	11:30	13:00	佐藤 隆	green製作所	□□商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-12-26	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
209	RPT-0092	G-3	3	47	2001	19	H	\N	\N	\N	\N	\N	2025-10-04	電子取引データ保存の相談	電子取引データの保存要件対応について相談を受け、社内規程整備を支援した。	\N	11:30	12:00	加藤 健一	さくら建設	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-05	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
210	RPT-0093	G-8	3	47	2001	13	M	\N	\N	\N	\N	\N	2026-07-01	賃上げ実施時期の相談	賃上げの実施時期と社会保険料負担への影響について相談があり、資金繰り計画の見直しとあわせて助成金活用を案内した。	\N	13:00	13:30	田中 太郎	松風食堂	○○商工会担当者	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-04	登録済み	20260809010939	\N	20260809010939	\N	\N	\N	\N
214	RPT-0096	G-2	3	01	0021	13	A	\N	\N	\N	\N	\N	2026-08-14	業務改善助成金の活用相談	最低賃金引き上げに伴う人件費増加について相談を受け、業務改善助成金を活用した設備投資を提案した。	\N	10:00	10:30	佐藤 太郎	佐藤農園	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-14	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
215	RPT-0097	G-3	3	01	0021	14	E	\N	\N	\N	\N	\N	2026-08-13	省力化投資に関する講習会	中小企業省力化投資補助金（カタログ型）の活用方法について事業者向け講習会を実施した。参加者からは対象設備の具体例について質問が多かった。	\N	13:30	15:00	鈴木 一郎	鈴木製作所	北海道商工会権限	高橋 由美	\N	\N	\N	\N	\N	\N	\N	2026-08-13	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
216	RPT-0098	G-4	3	01	0021	15	M	\N	\N	\N	\N	\N	2026-08-11	省エネ設備導入の専門家派遣	燃料費・電気代高騰への対応として、省エネ設備（高効率空調）導入に詳しい専門家を派遣し、投資回収シミュレーションを行った。	\N	14:00	15:30	伊藤 誠	旅館いとう	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-12	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
217	RPT-0099	G-5	3	01	0021	16	I	\N	\N	\N	\N	\N	2026-08-10	ITツール導入の個人相談会	受発注・在庫管理のクラウド化について個人相談会を実施し、IT導入補助金の申請要件を説明した。	\N	11:00	11:30	渡辺 香織	渡辺商店	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-10	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
218	RPT-0100	G-6	3	01	0021	17	H	\N	\N	\N	\N	\N	2026-08-08	輸出先多角化に関する研修会	米国関税の影響を受ける事業者向けに、輸出先多角化・海外展示会出展支援策の研修会を実施した。	\N	10:00	12:00	山本 直樹	山本運輸	北海道商工会権限	中村 美咲	\N	\N	\N	\N	\N	\N	\N	2026-08-08	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
219	RPT-0101	G-7	3	01	0021	18	D	\N	\N	\N	\N	\N	2026-08-06	インボイス制度対応の施策普及	適格請求書発行事業者登録がまだの事業者を個別訪問し、インボイス制度対応の必要書類・手続きを案内した。	\N	09:30	10:00	小林 健	小林建設	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-06	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
220	RPT-0102	G-8	3	01	0021	19	K	\N	\N	\N	\N	\N	2026-08-04	電子帳簿保存法対応の研修会実績	電子取引データ保存の要件対応をテーマにした研修会を開催し、社内規程整備のポイントを解説した。	\N	13:00	14:30	加藤 明美	加藤不動産	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-05	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
221	RPT-0103	G-2	3	01	0021	20	P	\N	\N	\N	\N	\N	2026-07-30	新型コロナ関連融資の相談	セーフティネット保証を活用した資金繰り相談を受け、返済計画の見直しを助言した。	\N	10:30	11:00	吉田 恵子	吉田医院	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-31	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
222	RPT-0104	G-3	3	01	0021	21	S	\N	\N	\N	\N	\N	2026-07-28	事業実施に係る事務処理の講習会	補助金申請時の証憑書類整理・事務処理の効率化について講習会を実施した。	\N	14:00	15:00	山田 修	山田福祉サービス	北海道商工会権限	佐々木 陽子	\N	\N	\N	\N	\N	\N	\N	2026-07-29	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
223	RPT-0105	G-4	3	01	0021	13	F	\N	\N	\N	\N	\N	2026-07-25	賃上げ促進税制の専門家派遣	賃上げ促進税制の適用要件について社会保険労務士を派遣し、必要な賃金台帳の整備を支援した。	\N	15:00	16:00	斎藤 大輔	斎藤電気工事	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-26	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
224	RPT-0106	G-5	3	01	0021	14	G	\N	\N	\N	\N	\N	2026-07-22	人手不足対応の個人相談会	業務フローの棚卸しと外部委託の可否について個人相談会で助言した。	\N	11:30	12:00	松本 弘	松本情報システム	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-23	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
225	RPT-0107	G-6	3	01	0021	15	J	\N	\N	\N	\N	\N	2026-07-20	エネルギーコスト見直しの研修会	複数年契約による電力調達コスト見直しをテーマに研修会を実施した。	\N	10:00	11:30	井上 学	いのうえ信用金庫	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-21	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
226	RPT-0108	G-7	3	01	0021	16	L	\N	\N	\N	\N	\N	2026-07-18	デジタル化施策の普及活動	キャッシュレス決済導入支援策について事業者を個別訪問し、導入費用の一部補助を案内した。	\N	09:00	09:30	木村 麻衣	木村コンサルティング	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-18	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
227	RPT-0109	G-8	3	01	0021	17	N	\N	\N	\N	\N	\N	2026-07-15	米国関税対応研修の実績	関税影響試算と価格転嫁交渉をテーマにした研修会を開催した。	\N	13:30	15:00	林 誠	林クリーニング	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-16	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
228	RPT-0110	G-2	3	01	0021	18	O	\N	\N	\N	\N	\N	2026-07-12	インボイス制度に関する相談	適格請求書の記載事項の誤りについて相談を受け、修正方法を助言した。	\N	10:00	10:30	清水 陽介	清水学習塾	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-13	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
229	RPT-0111	G-3	3	01	0021	19	Q	\N	\N	\N	\N	\N	2026-07-10	電子帳簿保存法の事業者向け講習会	検索要件を満たす電子データの保存方法について講習会を実施した。	\N	14:00	15:30	森田 有紀	森田コンサルティング	北海道商工会権限	田中 誠	\N	\N	\N	\N	\N	\N	\N	2026-07-10	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
230	RPT-0112	G-4	3	01	0021	20	R	\N	\N	\N	\N	\N	2026-07-08	感染症対策の専門家派遣	コロナ禍以降の感染症対策マニュアル整備について専門家を派遣し助言した。	\N	11:00	12:00	橋本 直子	橋本サービス	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-09	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
231	RPT-0113	G-5	3	01	0021	21	C	\N	\N	\N	\N	\N	2026-07-05	補助金事務処理の個人相談会	実績報告書の作成方法について個人相談会で個別に助言した。	\N	15:30	16:00	藤田 剛	藤田鉱業	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-06	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
232	RPT-0114	G-6	3	01	0021	14	T	\N	\N	\N	\N	\N	2026-07-03	人手不足対応の研修会	多能工化・兼務体制の整備をテーマに研修会を実施した。	\N	10:00	11:00	西村 智子	西村サービス	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-04	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
233	RPT-0115	G-7	3	01	0021	15	B	\N	\N	\N	\N	\N	2026-07-01	エネルギー価格高騰対策の普及	省エネルギー診断事業の案内と燃料費高騰対策の資金繰り相談窓口を紹介した。	\N	09:30	10:00	岡田 拓也	岡田水産	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-07-01	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
234	RPT-0116	F	3	01	0021	13	D	\N	\N	\N	\N	\N	2026-08-15	賃上げ実施時期の相談	最低賃金引き上げへの対応時期と資金繰りについて相談があり、業務改善助成金の活用を案内した。	\N	10:00	10:30	長谷川 淳	長谷川工務店	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-15	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
235	RPT-0117	F	3	01	0021	16	I	\N	\N	\N	\N	\N	2026-08-13	ECサイト構築の相談	販路拡大のためのECサイト構築について相談を受け、小規模事業者持続化補助金の活用を提案した。	\N	14:00	14:30	村上 恵	村上雑貨店	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-13	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
236	RPT-0118	F	3	01	0021	18	M	\N	\N	\N	\N	\N	2026-08-09	インボイス制度の登録相談	適格請求書発行事業者の登録手続きについて相談があり、必要書類の準備を助言した。	\N	11:00	11:30	石井 亮	石井旅館	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-09	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
237	RPT-0119	F	3	01	0021	15	H	\N	\N	\N	\N	\N	2026-08-05	燃料費高騰の資金繰り相談	燃料費・電気代高騰による資金繰り悪化について相談を受け、セーフティネット保証の活用を案内した。	\N	15:00	15:30	前田 裕子	前田運送	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-05	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
238	RPT-0120	F	3	01	0021	14	E	\N	\N	\N	\N	\N	2026-08-01	人手不足に関する相談	受注対応の遅れについて相談があり、省力化投資補助金の活用と業務フロー見直しを助言した。	\N	13:00	13:30	藤原 隆	藤原製作所	北海道商工会権限	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-01	登録済み	20260816224643	90	20260816224643	90	\N	\N	\N
239	RPT-0121	\N	3	01	0021	\N	\N	\N	\N	\N	\N	\N	2026-08-26			\N	22:38			佐藤農園	小島 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-26	下書き	20260826223833	90	20260826223833	90	\N	\N	\N
240	RPT-0122	\N	3	01	0021	\N	\N	\N	\N	\N	\N	\N	2026-08-26			\N	22:46				小島 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-26	下書き	20260826224610	90	20260826224610	90	\N	\N	\N
241	RPT-0123	F	3	20	2001	13	I	\N	\N	\N	\N	\N	2026-08-20	Playwright検証用の相談内容です。	Playwright検証用の相談内容です。	\N	10:00	11:00		テスト商店_PWCHECK	井上 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-27	削除	20260827071400	22	20260827071504	22	20260827071504	22	\N
242	RPT-0124	G-2	3	20	2001	13	I	\N	\N	\N	\N	\N	2026-08-20	Playwright検証用のG-2報告内容です。	Playwright検証用のG-2報告内容です。	\N	13:00	14:00		テスト商店_PWCHECK	井上 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-27	削除	20260827071401	22	20260827071505	22	20260827071505	22	\N
243	RPT-0125	G-2	3	20	2001	13	I	\N	\N	\N	\N	\N	2026-08-21	様式切替後の内容	様式切替後の内容	\N	09:00	09:30		テスト商店_PWCHECK2	井上 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-27	削除	20260827071442	22	20260827071507	22	20260827071507	22	\N
244	RPT-0126	\N	3	01	0021	\N	\N	\N	\N	\N	\N	\N	2026-08-27			\N	07:17			kabu	小島 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-27	下書き	20260827071832	90	20260827071832	90	\N	\N	\N
163	RPT-0046	G-4	3	20	2001	18	H	\N	\N	\N	\N	\N	2026-04-09	免税事業者との取引条件について相談があり、下請取引の留意点を助言した。	免税事業者との取引条件について相談があり、下請取引の留意点を助言した。	\N	15:00	16:00		第一工業	井上 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-11	下書き	20260809010939	\N	20260827073133	22	\N	\N	\N
245	RPT-0127	G-2	3	20	2001	13	I	\N	\N	\N	\N	\N	2026-08-22	編集して登録するテスト	編集して登録するテスト	\N	10:00	11:00		回帰テスト商店	井上 直樹	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-27	削除	20260827073335	22	20260827073336	22	20260827073336	22	\N
\.


--
-- Data for Name: trn_report_theme; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_report_theme (report_id, theme_id) FROM stdin;
118	19
119	18
120	20
121	14
122	13
123	16
124	18
125	21
126	14
127	14
128	20
129	18
130	15
131	14
132	16
133	21
134	21
135	18
136	20
137	17
138	20
139	13
140	15
141	17
142	19
143	21
144	13
145	21
146	19
147	13
148	13
149	21
150	13
151	16
152	20
153	14
154	13
155	19
156	21
157	16
158	13
159	15
160	16
161	16
162	17
164	19
165	20
166	13
167	16
168	17
169	15
170	15
171	19
172	13
173	20
174	14
175	21
176	16
177	17
178	19
179	20
180	16
181	15
182	18
183	13
184	17
185	21
186	15
187	19
188	21
189	18
190	17
191	13
192	20
193	14
194	15
195	18
196	17
197	20
198	19
199	13
200	13
201	15
202	17
203	17
204	16
205	20
206	14
207	19
208	20
209	19
210	13
212	14
212	15
212	19
211	13
241	13
242	13
243	13
163	18
245	13
\.


--
-- Data for Name: trn_trusted_device; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_trusted_device (trusted_device_id, user_account_id, token_hash, created_at, expires_at) FROM stdin;
1	1	eb04a2f48615a31a0d92ce1c2ab7caee70e80a86188b40088149cbaa68669f8d	20260802185731	2026-09-01 18:57:31.64877+09
2	14	de5bff3cf6f715513a41c1c84ab42df83c7998f1a2d87d82cb571d58cdf2009b	20260804234427	2026-09-03 23:44:27.934959+09
3	1	b807a96feae02bb8c5b7bd7f1cb0a915cf1635a4ec550efff3a857ae28c2ef07	20260804235817	2026-09-03 23:58:17.793417+09
4	2	3f4623aff146eb73758b528a04f3003143b84c72c2b84120886e9d2868311949	20260805001627	2026-09-04 00:16:27.540496+09
5	1	86b901bbe61a894f316e7f66d67a93383f6e034859fcd3494276cc62642baa8f	20260805001636	2026-09-04 00:16:36.089982+09
6	14	5a33c95d37479ab5c89df596293c7195f204bf6461717d5169e207741b5db9f6	20260805003728	2026-09-04 00:37:28.62073+09
7	2	c927154c908d829eba64c45fdcdcec0e1205b8b796c40aad1497c383f953702f	20260805003927	2026-09-04 00:39:27.727247+09
8	14	770461093d700d224359d365c6546778f599a2e543d938b3012b1b1ef3f6450f	20260805080550	2026-09-04 08:05:50.554666+09
9	1	bb669875e0805652f1952e1c25efaf284a0089d2fc04c31b00483f52cd7ce434	20260806230619	2026-09-05 23:06:19.787663+09
10	2	817c50560d5e6dc4a15fa02721cf60d2e922d9f03d94acdc28254feee4c3531a	20260806233351	2026-09-05 23:33:51.400082+09
11	3	731db1b3a7f78e653603b7fbdab76bb2f7ce0cad30ba435ebb480fd0bf3b28ab	20260807001559	2026-09-06 00:15:59.269068+09
12	89	111e1478a615821bf2b195985367e59ac86f691949326cc0517fbba86c2d67ef	20260812092606	2026-08-27 09:26:06.744087+09
13	90	642285bc733884aa0a74161afca65cfe3d84daf988c6f972f874c1b256a24523	20260812092634	2026-08-27 09:26:34.641992+09
14	1	9ff9ae9c81548673a954e3dcbcc74fa2911a361e4a1f2f3fa34a4b246f409a32	20260826074523	2026-09-10 07:45:23.577201+09
15	90	93469e490bca5a13ede8ed6044d4961917eecb8e47a64529374c0ab496606c31	20260826214717	2026-09-10 21:47:17.856802+09
16	89	1af8b1363125b3855700e212b6e951c6ea0194af3cd3eae2954b45bf93a031e6	20260826220032	2026-09-10 22:00:32.295579+09
17	1	d15d7a0b509e5985af927338d3c77871f364c044057fbb7251792375d627529e	20260826220222	2026-09-10 22:02:22.94076+09
18	90	39c93460e8c3e6c137947f79fe94f52668902c5caffb65843f539e8f38579eae	20260826221944	2026-09-10 22:19:44.712117+09
19	1	c78cff857e0cc47f7fb2ea351c6a0c199381e9e694ac64bfd14127ffa2ca250e	20260826222341	2026-09-10 22:23:41.966294+09
20	90	93668ecda0f207de115aee9dd607a9e80194ffe64f987194eab584d3588ed885	20260826223807	2026-09-10 22:38:07.741949+09
21	89	e82fa1c96aedaf7d8ea852a18a01666d7d8cc18df219917588769ea9644f1a9e	20260827072308	2026-09-11 07:23:08.209766+09
22	1	fad53c8ecbbe25898c4ad2aa1fa567ba291fa39d3253f44de65bb970c564183b	20260827072325	2026-09-11 07:23:25.552278+09
23	89	1a4fb2a20ea9fc2a4f3435993662ffbcb49bd6605765ead09d23cb8c57646d64	20260827074516	2026-08-28 07:45:16.762478+09
\.


--
-- Data for Name: trn_vector_collection; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trn_vector_collection (vector_collection_id, rag_setting_id, collection_code, name, vector_count, baseline_vector_count, status, synced_date, created_at, created_by, updated_at, updated_by, deleted_at, deleted_by) FROM stdin;
1	1	col-001	法令・制度	4822	4820	同期済み	2026-08-09	20260808115851	\N	20260809003457	1	\N	\N
2	1	col-002	税制	6210	6210	同期済み	2026-08-09	20260808115851	\N	20260809003457	1	\N	\N
3	1	col-003	補助金	3982	3980	同期済み	2026-08-09	20260808115851	\N	20260809003457	1	\N	\N
4	1	col-004	経営支援	2141	2140	同期済み	2026-08-09	20260808115851	\N	20260809003457	1	\N	\N
5	1	col-005	テストコレクション	10	10	同期済み	2026-08-09	20260808115851	\N	20260809003457	1	\N	\N
6	1	col-006	リファクタ後コレクション	5	5	同期済み	2026-08-09	20260808115851	\N	20260809003457	1	\N	\N
\.


--
-- Name: cfg_excel_output_mapping_mapping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cfg_excel_output_mapping_mapping_id_seq', 239, true);


--
-- Name: cfg_rag_setting_rag_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cfg_rag_setting_rag_setting_id_seq', 1, true);


--
-- Name: mst_capital_range_capital_range_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_capital_range_capital_range_id_seq', 4, true);


--
-- Name: mst_employee_range_employee_range_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_employee_range_employee_range_id_seq', 4, true);


--
-- Name: mst_fiscal_year_fiscal_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_fiscal_year_fiscal_year_id_seq', 3, true);


--
-- Name: mst_qualification_qualification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_qualification_qualification_id_seq', 2, true);


--
-- Name: mst_revenue_range_revenue_range_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_revenue_range_revenue_range_id_seq', 4, true);


--
-- Name: mst_theme_theme_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_theme_theme_id_seq1', 21, true);


--
-- Name: mst_user_account_user_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_user_account_user_account_id_seq', 94, true);


--
-- Name: mst_visit_result_visit_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mst_visit_result_visit_result_id_seq', 4, true);


--
-- Name: trn_ai_usage_log_ai_usage_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_ai_usage_log_ai_usage_log_id_seq', 40, true);


--
-- Name: trn_change_history_change_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_change_history_change_history_id_seq', 200, true);


--
-- Name: trn_knowledge_document_knowledge_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_knowledge_document_knowledge_document_id_seq', 9, true);


--
-- Name: trn_knowledge_document_versio_knowledge_document_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_knowledge_document_versio_knowledge_document_version_id_seq', 17, true);


--
-- Name: trn_knowledge_entry_knowledge_entry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_knowledge_entry_knowledge_entry_id_seq', 14, true);


--
-- Name: trn_kpi_monthly_stat_kpi_monthly_stat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_kpi_monthly_stat_kpi_monthly_stat_id_seq', 2434, true);


--
-- Name: trn_kpi_theme_breakdown_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_kpi_theme_breakdown_id_seq', 1297, true);


--
-- Name: trn_notice_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_notice_notice_id_seq', 50, true);


--
-- Name: trn_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_report_report_id_seq', 245, true);


--
-- Name: trn_trusted_device_trusted_device_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_trusted_device_trusted_device_id_seq', 23, true);


--
-- Name: trn_vector_collection_vector_collection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trn_vector_collection_vector_collection_id_seq', 6, true);


--
-- Name: mst_capital_range mst_capital_range_fiscal_year_id_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_capital_range
    ADD CONSTRAINT mst_capital_range_fiscal_year_id_code_key UNIQUE (fiscal_year_id, capital_range_code);


--
-- Name: mst_capital_range mst_capital_range_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_capital_range
    ADD CONSTRAINT mst_capital_range_pkey PRIMARY KEY (capital_range_id);


--
-- Name: mst_employee_range mst_employee_count_range_fiscal_year_id_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_employee_range
    ADD CONSTRAINT mst_employee_count_range_fiscal_year_id_code_key UNIQUE (fiscal_year_id, employee_range_code);


--
-- Name: mst_employee_range mst_employee_count_range_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_employee_range
    ADD CONSTRAINT mst_employee_count_range_pkey PRIMARY KEY (employee_range_id);


--
-- Name: cfg_excel_output_mapping mst_excel_output_mapping_form_slot_column_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_excel_output_mapping
    ADD CONSTRAINT mst_excel_output_mapping_form_slot_column_key UNIQUE (form_code, fiscal_year_id, slot_number, view_column);


--
-- Name: cfg_excel_output_mapping mst_excel_output_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_excel_output_mapping
    ADD CONSTRAINT mst_excel_output_mapping_pkey PRIMARY KEY (mapping_id);


--
-- Name: cfg_excel_report_definition mst_excel_report_definition_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_excel_report_definition
    ADD CONSTRAINT mst_excel_report_definition_pkey PRIMARY KEY (form_code, fiscal_year_id);


--
-- Name: mst_fiscal_year mst_fiscal_year_fiscal_year_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_fiscal_year
    ADD CONSTRAINT mst_fiscal_year_fiscal_year_code_key UNIQUE (fiscal_year_code);


--
-- Name: mst_fiscal_year mst_fiscal_year_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_fiscal_year
    ADD CONSTRAINT mst_fiscal_year_pkey PRIMARY KEY (fiscal_year_id);


--
-- Name: mst_form mst_form_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_form
    ADD CONSTRAINT mst_form_pkey1 PRIMARY KEY (form_code, fiscal_year_id);


--
-- Name: mst_industry mst_industry_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_industry
    ADD CONSTRAINT mst_industry_pkey1 PRIMARY KEY (industry_code, fiscal_year_id);


--
-- Name: trn_knowledge_document_version mst_knowledge_document_versio_knowledge_document_id_version_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version
    ADD CONSTRAINT mst_knowledge_document_versio_knowledge_document_id_version_key UNIQUE (knowledge_document_id, version_number);


--
-- Name: trn_knowledge_document_version mst_knowledge_document_version_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version
    ADD CONSTRAINT mst_knowledge_document_version_pkey PRIMARY KEY (knowledge_document_version_id);


--
-- Name: cfg_menu_item mst_menu_item_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_menu_item
    ADD CONSTRAINT mst_menu_item_pkey1 PRIMARY KEY (role_code, section_sort_order, sort_order);


--
-- Name: mst_prefecture mst_prefecture_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_prefecture
    ADD CONSTRAINT mst_prefecture_pkey PRIMARY KEY (prefecture_code);


--
-- Name: mst_prefecture mst_prefecture_sort_order_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_prefecture
    ADD CONSTRAINT mst_prefecture_sort_order_key UNIQUE (sort_order);


--
-- Name: mst_qualification mst_qualification_fiscal_year_id_qualification_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_qualification
    ADD CONSTRAINT mst_qualification_fiscal_year_id_qualification_code_key UNIQUE (fiscal_year_id, qualification_code);


--
-- Name: mst_qualification mst_qualification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_qualification
    ADD CONSTRAINT mst_qualification_pkey PRIMARY KEY (qualification_id);


--
-- Name: cfg_rag_setting mst_rag_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_rag_setting
    ADD CONSTRAINT mst_rag_setting_pkey PRIMARY KEY (rag_setting_id);


--
-- Name: mst_revenue_range mst_revenue_range_fiscal_year_id_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_revenue_range
    ADD CONSTRAINT mst_revenue_range_fiscal_year_id_code_key UNIQUE (fiscal_year_id, revenue_range_code);


--
-- Name: mst_revenue_range mst_revenue_range_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_revenue_range
    ADD CONSTRAINT mst_revenue_range_pkey PRIMARY KEY (revenue_range_id);


--
-- Name: mst_shokokai mst_shokokai_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_shokokai
    ADD CONSTRAINT mst_shokokai_pkey PRIMARY KEY (prefecture_code, shokokai_cd);


--
-- Name: cfg_system_setting mst_system_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_system_setting
    ADD CONSTRAINT mst_system_setting_pkey PRIMARY KEY (setting_code);


--
-- Name: mst_theme mst_theme_fiscal_year_id_theme_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme
    ADD CONSTRAINT mst_theme_fiscal_year_id_theme_code_key UNIQUE (fiscal_year_id, theme_code);


--
-- Name: mst_theme mst_theme_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme
    ADD CONSTRAINT mst_theme_pkey1 PRIMARY KEY (theme_id);


--
-- Name: mst_user_account mst_user_account_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account
    ADD CONSTRAINT mst_user_account_pkey PRIMARY KEY (user_account_id);


--
-- Name: mst_user_account mst_user_account_prefecture_code_staff_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account
    ADD CONSTRAINT mst_user_account_prefecture_code_staff_code_key UNIQUE (prefecture_code, user_id);


--
-- Name: mst_user_account_qualification mst_user_account_qualification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account_qualification
    ADD CONSTRAINT mst_user_account_qualification_pkey PRIMARY KEY (user_account_id, qualification_id);


--
-- Name: mst_visit_result mst_visit_result_fiscal_year_id_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_visit_result
    ADD CONSTRAINT mst_visit_result_fiscal_year_id_code_key UNIQUE (fiscal_year_id, visit_result_code);


--
-- Name: mst_visit_result mst_visit_result_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_visit_result
    ADD CONSTRAINT mst_visit_result_pkey PRIMARY KEY (visit_result_id);


--
-- Name: trn_ai_usage_log trn_ai_usage_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_ai_usage_log
    ADD CONSTRAINT trn_ai_usage_log_pkey PRIMARY KEY (ai_usage_log_id);


--
-- Name: trn_change_history trn_change_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_change_history
    ADD CONSTRAINT trn_change_history_pkey PRIMARY KEY (change_history_id);


--
-- Name: trn_knowledge_document trn_knowledge_document_new_document_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT trn_knowledge_document_new_document_code_key UNIQUE (document_code);


--
-- Name: trn_knowledge_document trn_knowledge_document_new_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT trn_knowledge_document_new_pkey PRIMARY KEY (knowledge_document_id);


--
-- Name: trn_knowledge_entry trn_knowledge_entry_new_knowledge_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT trn_knowledge_entry_new_knowledge_code_key UNIQUE (knowledge_code);


--
-- Name: trn_knowledge_entry trn_knowledge_entry_new_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT trn_knowledge_entry_new_pkey PRIMARY KEY (knowledge_entry_id);


--
-- Name: trn_knowledge_entry_theme trn_knowledge_entry_theme_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry_theme
    ADD CONSTRAINT trn_knowledge_entry_theme_pkey PRIMARY KEY (knowledge_entry_id, theme_id);


--
-- Name: trn_kpi_monthly_stat trn_kpi_monthly_stat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT trn_kpi_monthly_stat_pkey PRIMARY KEY (kpi_monthly_stat_id);


--
-- Name: trn_kpi_monthly_stat trn_kpi_monthly_stat_prefecture_code_shokokai_cd_fiscal_year_ke; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT trn_kpi_monthly_stat_prefecture_code_shokokai_cd_fiscal_year_ke UNIQUE NULLS NOT DISTINCT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, year_month);


--
-- Name: trn_kpi_theme_breakdown trn_kpi_theme_breakdown_new_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT trn_kpi_theme_breakdown_new_pkey PRIMARY KEY (id);


--
-- Name: trn_kpi_theme_breakdown trn_kpi_theme_breakdown_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT trn_kpi_theme_breakdown_unique UNIQUE (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month);


--
-- Name: trn_notice trn_notice_notice_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_notice
    ADD CONSTRAINT trn_notice_notice_code_key UNIQUE (notice_code);


--
-- Name: trn_notice trn_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_notice
    ADD CONSTRAINT trn_notice_pkey PRIMARY KEY (notice_id);


--
-- Name: trn_report trn_report_new_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_pkey PRIMARY KEY (report_id);


--
-- Name: trn_report trn_report_new_report_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_report_code_key UNIQUE (report_code);


--
-- Name: trn_report_theme trn_report_theme_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report_theme
    ADD CONSTRAINT trn_report_theme_pkey PRIMARY KEY (report_id, theme_id);


--
-- Name: trn_trusted_device trn_trusted_device_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_trusted_device
    ADD CONSTRAINT trn_trusted_device_pkey PRIMARY KEY (trusted_device_id);


--
-- Name: trn_trusted_device trn_trusted_device_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_trusted_device
    ADD CONSTRAINT trn_trusted_device_token_hash_key UNIQUE (token_hash);


--
-- Name: trn_vector_collection trn_vector_collection_new_collection_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection
    ADD CONSTRAINT trn_vector_collection_new_collection_code_key UNIQUE (collection_code);


--
-- Name: trn_vector_collection trn_vector_collection_new_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection
    ADD CONSTRAINT trn_vector_collection_new_pkey PRIMARY KEY (vector_collection_id);


--
-- Name: idx_mst_capital_range_fiscal_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_capital_range_fiscal_year ON public.mst_capital_range USING btree (fiscal_year_id);


--
-- Name: idx_mst_employee_range_fiscal_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_employee_range_fiscal_year ON public.mst_employee_range USING btree (fiscal_year_id);


--
-- Name: idx_mst_qualification_fiscal_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_qualification_fiscal_year ON public.mst_qualification USING btree (fiscal_year_id);


--
-- Name: idx_mst_revenue_range_fiscal_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_revenue_range_fiscal_year ON public.mst_revenue_range USING btree (fiscal_year_id);


--
-- Name: idx_mst_theme_fiscal_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_theme_fiscal_year ON public.mst_theme USING btree (fiscal_year_id);


--
-- Name: idx_mst_user_account_login; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_user_account_login ON public.mst_user_account USING btree (prefecture_code, lower(user_id)) WHERE (status = 1);


--
-- Name: idx_mst_user_account_shokokai; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_user_account_shokokai ON public.mst_user_account USING btree (prefecture_code, shokokai_cd);


--
-- Name: idx_mst_visit_result_fiscal_year; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_mst_visit_result_fiscal_year ON public.mst_visit_result USING btree (fiscal_year_id);


--
-- Name: idx_trn_ai_usage_log_feature; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_ai_usage_log_feature ON public.trn_ai_usage_log USING btree (feature);


--
-- Name: idx_trn_ai_usage_log_user_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_ai_usage_log_user_date ON public.trn_ai_usage_log USING btree (user_account_id, used_at DESC);


--
-- Name: idx_trn_change_history_changed_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_change_history_changed_at ON public.trn_change_history USING btree (changed_at DESC);


--
-- Name: idx_trn_change_history_changed_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_change_history_changed_by ON public.trn_change_history USING btree (changed_by);


--
-- Name: idx_trn_change_history_table_record; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_change_history_table_record ON public.trn_change_history USING btree (table_name, record_id);


--
-- Name: idx_trn_knowledge_document_prefecture; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_knowledge_document_prefecture ON public.trn_knowledge_document USING btree (prefecture_code);


--
-- Name: idx_trn_knowledge_entry_document; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_knowledge_entry_document ON public.trn_knowledge_entry USING btree (knowledge_document_id);


--
-- Name: idx_trn_knowledge_entry_prefecture; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_knowledge_entry_prefecture ON public.trn_knowledge_entry USING btree (prefecture_code);


--
-- Name: idx_trn_kpi_monthly_stat_dashboard; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_kpi_monthly_stat_dashboard ON public.trn_kpi_monthly_stat USING btree (prefecture_code, shokokai_cd, fiscal_year_id, year_month);


--
-- Name: idx_trn_notice_role; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_notice_role ON public.trn_notice USING btree (role_code);


--
-- Name: idx_trn_report_form; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_report_form ON public.trn_report USING btree (form_code, fiscal_year_id);


--
-- Name: idx_trn_report_industry; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_report_industry ON public.trn_report USING btree (industry_code, fiscal_year_id);


--
-- Name: idx_trn_report_shokokai; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_report_shokokai ON public.trn_report USING btree (prefecture_code, shokokai_cd);


--
-- Name: idx_trn_report_status_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_report_status_date ON public.trn_report USING btree (status, report_date DESC, registered_at DESC);


--
-- Name: idx_trn_report_theme; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_report_theme ON public.trn_report USING btree (theme_id);


--
-- Name: idx_trn_trusted_device_user_account; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_trusted_device_user_account ON public.trn_trusted_device USING btree (user_account_id);


--
-- Name: idx_trn_vector_collection_setting; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_trn_vector_collection_setting ON public.trn_vector_collection USING btree (rag_setting_id);


--
-- Name: cfg_menu_item fk_cfg_menu_item_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_menu_item
    ADD CONSTRAINT fk_cfg_menu_item_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_menu_item fk_cfg_menu_item_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_menu_item
    ADD CONSTRAINT fk_cfg_menu_item_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_menu_item fk_cfg_menu_item_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_menu_item
    ADD CONSTRAINT fk_cfg_menu_item_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_rag_setting fk_cfg_rag_setting_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_rag_setting
    ADD CONSTRAINT fk_cfg_rag_setting_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_rag_setting fk_cfg_rag_setting_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_rag_setting
    ADD CONSTRAINT fk_cfg_rag_setting_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_rag_setting fk_cfg_rag_setting_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_rag_setting
    ADD CONSTRAINT fk_cfg_rag_setting_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_system_setting fk_cfg_system_setting_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_system_setting
    ADD CONSTRAINT fk_cfg_system_setting_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_system_setting fk_cfg_system_setting_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_system_setting
    ADD CONSTRAINT fk_cfg_system_setting_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: cfg_system_setting fk_cfg_system_setting_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_system_setting
    ADD CONSTRAINT fk_cfg_system_setting_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_fiscal_year fk_mst_fiscal_year_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_fiscal_year
    ADD CONSTRAINT fk_mst_fiscal_year_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_fiscal_year fk_mst_fiscal_year_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_fiscal_year
    ADD CONSTRAINT fk_mst_fiscal_year_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_fiscal_year fk_mst_fiscal_year_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_fiscal_year
    ADD CONSTRAINT fk_mst_fiscal_year_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_form fk_mst_form_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_form
    ADD CONSTRAINT fk_mst_form_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_form fk_mst_form_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_form
    ADD CONSTRAINT fk_mst_form_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_form fk_mst_form_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_form
    ADD CONSTRAINT fk_mst_form_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_industry fk_mst_industry_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_industry
    ADD CONSTRAINT fk_mst_industry_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_industry fk_mst_industry_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_industry
    ADD CONSTRAINT fk_mst_industry_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_industry fk_mst_industry_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_industry
    ADD CONSTRAINT fk_mst_industry_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_prefecture fk_mst_prefecture_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_prefecture
    ADD CONSTRAINT fk_mst_prefecture_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_prefecture fk_mst_prefecture_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_prefecture
    ADD CONSTRAINT fk_mst_prefecture_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_prefecture fk_mst_prefecture_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_prefecture
    ADD CONSTRAINT fk_mst_prefecture_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_shokokai fk_mst_shokokai_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_shokokai
    ADD CONSTRAINT fk_mst_shokokai_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_shokokai fk_mst_shokokai_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_shokokai
    ADD CONSTRAINT fk_mst_shokokai_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_shokokai fk_mst_shokokai_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_shokokai
    ADD CONSTRAINT fk_mst_shokokai_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_theme fk_mst_theme_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme
    ADD CONSTRAINT fk_mst_theme_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_theme fk_mst_theme_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme
    ADD CONSTRAINT fk_mst_theme_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_theme fk_mst_theme_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme
    ADD CONSTRAINT fk_mst_theme_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_user_account fk_mst_user_account_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account
    ADD CONSTRAINT fk_mst_user_account_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_user_account fk_mst_user_account_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account
    ADD CONSTRAINT fk_mst_user_account_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_user_account fk_mst_user_account_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account
    ADD CONSTRAINT fk_mst_user_account_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document fk_trn_knowledge_document_active_version; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT fk_trn_knowledge_document_active_version FOREIGN KEY (knowledge_document_id, active_version_number) REFERENCES public.trn_knowledge_document_version(knowledge_document_id, version_number) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trn_knowledge_document fk_trn_knowledge_document_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT fk_trn_knowledge_document_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document fk_trn_knowledge_document_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT fk_trn_knowledge_document_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document fk_trn_knowledge_document_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT fk_trn_knowledge_document_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document_version fk_trn_knowledge_document_version_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version
    ADD CONSTRAINT fk_trn_knowledge_document_version_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document_version fk_trn_knowledge_document_version_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version
    ADD CONSTRAINT fk_trn_knowledge_document_version_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document_version fk_trn_knowledge_document_version_document; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version
    ADD CONSTRAINT fk_trn_knowledge_document_version_document FOREIGN KEY (knowledge_document_id) REFERENCES public.trn_knowledge_document(knowledge_document_id) ON DELETE CASCADE;


--
-- Name: trn_knowledge_document_version fk_trn_knowledge_document_version_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document_version
    ADD CONSTRAINT fk_trn_knowledge_document_version_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_entry fk_trn_knowledge_entry_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT fk_trn_knowledge_entry_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_entry fk_trn_knowledge_entry_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT fk_trn_knowledge_entry_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_entry_theme fk_trn_knowledge_entry_theme_entry; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry_theme
    ADD CONSTRAINT fk_trn_knowledge_entry_theme_entry FOREIGN KEY (knowledge_entry_id) REFERENCES public.trn_knowledge_entry(knowledge_entry_id);


--
-- Name: trn_knowledge_entry fk_trn_knowledge_entry_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT fk_trn_knowledge_entry_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_kpi_monthly_stat fk_trn_kpi_monthly_stat_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT fk_trn_kpi_monthly_stat_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_kpi_monthly_stat fk_trn_kpi_monthly_stat_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT fk_trn_kpi_monthly_stat_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_kpi_monthly_stat fk_trn_kpi_monthly_stat_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT fk_trn_kpi_monthly_stat_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_kpi_theme_breakdown fk_trn_kpi_theme_breakdown_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT fk_trn_kpi_theme_breakdown_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_kpi_theme_breakdown fk_trn_kpi_theme_breakdown_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT fk_trn_kpi_theme_breakdown_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_kpi_theme_breakdown fk_trn_kpi_theme_breakdown_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT fk_trn_kpi_theme_breakdown_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_notice fk_trn_notice_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_notice
    ADD CONSTRAINT fk_trn_notice_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_notice fk_trn_notice_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_notice
    ADD CONSTRAINT fk_trn_notice_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_notice fk_trn_notice_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_notice
    ADD CONSTRAINT fk_trn_notice_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_report fk_trn_report_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT fk_trn_report_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_report fk_trn_report_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT fk_trn_report_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_report fk_trn_report_industry; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT fk_trn_report_industry FOREIGN KEY (industry_code, fiscal_year_id) REFERENCES public.mst_industry(industry_code, fiscal_year_id);


--
-- Name: trn_report fk_trn_report_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT fk_trn_report_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_vector_collection fk_trn_vector_collection_created_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection
    ADD CONSTRAINT fk_trn_vector_collection_created_by FOREIGN KEY (created_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_vector_collection fk_trn_vector_collection_deleted_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection
    ADD CONSTRAINT fk_trn_vector_collection_deleted_by FOREIGN KEY (deleted_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_vector_collection fk_trn_vector_collection_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection
    ADD CONSTRAINT fk_trn_vector_collection_updated_by FOREIGN KEY (updated_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_capital_range mst_capital_range_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_capital_range
    ADD CONSTRAINT mst_capital_range_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: mst_employee_range mst_employee_count_range_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_employee_range
    ADD CONSTRAINT mst_employee_count_range_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: cfg_excel_output_mapping mst_excel_output_mapping_form_code_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_excel_output_mapping
    ADD CONSTRAINT mst_excel_output_mapping_form_code_fiscal_year_id_fkey FOREIGN KEY (form_code, fiscal_year_id) REFERENCES public.cfg_excel_report_definition(form_code, fiscal_year_id);


--
-- Name: cfg_excel_report_definition mst_excel_report_definition_form_code_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cfg_excel_report_definition
    ADD CONSTRAINT mst_excel_report_definition_form_code_fiscal_year_id_fkey FOREIGN KEY (form_code, fiscal_year_id) REFERENCES public.mst_form(form_code, fiscal_year_id);


--
-- Name: mst_form mst_form_fiscal_year_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_form
    ADD CONSTRAINT mst_form_fiscal_year_id_fkey1 FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: mst_industry mst_industry_fiscal_year_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_industry
    ADD CONSTRAINT mst_industry_fiscal_year_id_fkey1 FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: mst_qualification mst_qualification_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_qualification
    ADD CONSTRAINT mst_qualification_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: mst_revenue_range mst_revenue_range_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_revenue_range
    ADD CONSTRAINT mst_revenue_range_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: mst_shokokai mst_shokokai_prefecture_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_shokokai
    ADD CONSTRAINT mst_shokokai_prefecture_code_fkey FOREIGN KEY (prefecture_code) REFERENCES public.mst_prefecture(prefecture_code);


--
-- Name: mst_theme mst_theme_fiscal_year_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_theme
    ADD CONSTRAINT mst_theme_fiscal_year_id_fkey1 FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: mst_user_account mst_user_account_prefecture_code_shokokai_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account
    ADD CONSTRAINT mst_user_account_prefecture_code_shokokai_code_fkey FOREIGN KEY (prefecture_code, shokokai_cd) REFERENCES public.mst_shokokai(prefecture_code, shokokai_cd);


--
-- Name: mst_user_account_qualification mst_user_account_qualification_qualification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account_qualification
    ADD CONSTRAINT mst_user_account_qualification_qualification_id_fkey FOREIGN KEY (qualification_id) REFERENCES public.mst_qualification(qualification_id);


--
-- Name: mst_user_account_qualification mst_user_account_qualification_user_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_user_account_qualification
    ADD CONSTRAINT mst_user_account_qualification_user_account_id_fkey FOREIGN KEY (user_account_id) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: mst_visit_result mst_visit_result_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mst_visit_result
    ADD CONSTRAINT mst_visit_result_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: trn_ai_usage_log trn_ai_usage_log_user_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_ai_usage_log
    ADD CONSTRAINT trn_ai_usage_log_user_account_id_fkey FOREIGN KEY (user_account_id) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_change_history trn_change_history_changed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_change_history
    ADD CONSTRAINT trn_change_history_changed_by_fkey FOREIGN KEY (changed_by) REFERENCES public.mst_user_account(user_account_id);


--
-- Name: trn_knowledge_document trn_knowledge_document_new_prefecture_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_document
    ADD CONSTRAINT trn_knowledge_document_new_prefecture_code_fkey FOREIGN KEY (prefecture_code) REFERENCES public.mst_prefecture(prefecture_code);


--
-- Name: trn_knowledge_entry trn_knowledge_entry_new_knowledge_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT trn_knowledge_entry_new_knowledge_document_id_fkey FOREIGN KEY (knowledge_document_id) REFERENCES public.trn_knowledge_document(knowledge_document_id) ON DELETE SET NULL;


--
-- Name: trn_knowledge_entry trn_knowledge_entry_new_prefecture_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry
    ADD CONSTRAINT trn_knowledge_entry_new_prefecture_code_fkey FOREIGN KEY (prefecture_code) REFERENCES public.mst_prefecture(prefecture_code);


--
-- Name: trn_knowledge_entry_theme trn_knowledge_entry_theme_theme_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_knowledge_entry_theme
    ADD CONSTRAINT trn_knowledge_entry_theme_theme_id_fkey FOREIGN KEY (theme_id) REFERENCES public.mst_theme(theme_id);


--
-- Name: trn_kpi_monthly_stat trn_kpi_monthly_stat_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT trn_kpi_monthly_stat_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: trn_kpi_monthly_stat trn_kpi_monthly_stat_prefecture_code_shokokai_cd_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT trn_kpi_monthly_stat_prefecture_code_shokokai_cd_fkey FOREIGN KEY (prefecture_code, shokokai_cd) REFERENCES public.mst_shokokai(prefecture_code, shokokai_cd);


--
-- Name: trn_kpi_monthly_stat trn_kpi_monthly_stat_prefecture_code_target_shokokai_cd_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT trn_kpi_monthly_stat_prefecture_code_target_shokokai_cd_fkey FOREIGN KEY (prefecture_code, target_shokokai_cd) REFERENCES public.mst_shokokai(prefecture_code, shokokai_cd);


--
-- Name: trn_kpi_monthly_stat trn_kpi_monthly_stat_target_prefecture_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_monthly_stat
    ADD CONSTRAINT trn_kpi_monthly_stat_target_prefecture_code_fkey FOREIGN KEY (target_prefecture_code) REFERENCES public.mst_prefecture(prefecture_code);


--
-- Name: trn_kpi_theme_breakdown trn_kpi_theme_breakdown_new_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT trn_kpi_theme_breakdown_new_fiscal_year_id_fkey FOREIGN KEY (fiscal_year_id) REFERENCES public.mst_fiscal_year(fiscal_year_id);


--
-- Name: trn_kpi_theme_breakdown trn_kpi_theme_breakdown_new_prefecture_code_shokokai_cd_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT trn_kpi_theme_breakdown_new_prefecture_code_shokokai_cd_fkey FOREIGN KEY (prefecture_code, shokokai_cd) REFERENCES public.mst_shokokai(prefecture_code, shokokai_cd);


--
-- Name: trn_kpi_theme_breakdown trn_kpi_theme_breakdown_new_theme_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_kpi_theme_breakdown
    ADD CONSTRAINT trn_kpi_theme_breakdown_new_theme_id_fkey FOREIGN KEY (theme_id) REFERENCES public.mst_theme(theme_id);


--
-- Name: trn_report trn_report_form_code_fiscal_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_form_code_fiscal_year_id_fkey FOREIGN KEY (form_code, fiscal_year_id) REFERENCES public.mst_form(form_code, fiscal_year_id);


--
-- Name: trn_report trn_report_new_capital_range_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_capital_range_id_fkey FOREIGN KEY (capital_range_id) REFERENCES public.mst_capital_range(capital_range_id);


--
-- Name: trn_report trn_report_new_employee_range_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_employee_range_id_fkey FOREIGN KEY (employee_range_id) REFERENCES public.mst_employee_range(employee_range_id);


--
-- Name: trn_report trn_report_new_expert_qualification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_expert_qualification_id_fkey FOREIGN KEY (expert_qualification_id) REFERENCES public.mst_qualification(qualification_id);


--
-- Name: trn_report trn_report_new_revenue_range_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_revenue_range_id_fkey FOREIGN KEY (revenue_range_id) REFERENCES public.mst_revenue_range(revenue_range_id);


--
-- Name: trn_report trn_report_new_theme_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_theme_id_fkey FOREIGN KEY (theme_id) REFERENCES public.mst_theme(theme_id);


--
-- Name: trn_report trn_report_new_visit_result_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_new_visit_result_id_fkey FOREIGN KEY (visit_result_id) REFERENCES public.mst_visit_result(visit_result_id);


--
-- Name: trn_report trn_report_prefecture_code_shokokai_cd_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report
    ADD CONSTRAINT trn_report_prefecture_code_shokokai_cd_fkey FOREIGN KEY (prefecture_code, shokokai_cd) REFERENCES public.mst_shokokai(prefecture_code, shokokai_cd);


--
-- Name: trn_report_theme trn_report_theme_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report_theme
    ADD CONSTRAINT trn_report_theme_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.trn_report(report_id);


--
-- Name: trn_report_theme trn_report_theme_theme_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_report_theme
    ADD CONSTRAINT trn_report_theme_theme_id_fkey FOREIGN KEY (theme_id) REFERENCES public.mst_theme(theme_id);


--
-- Name: trn_trusted_device trn_trusted_device_user_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_trusted_device
    ADD CONSTRAINT trn_trusted_device_user_account_id_fkey FOREIGN KEY (user_account_id) REFERENCES public.mst_user_account(user_account_id) ON DELETE CASCADE;


--
-- Name: trn_vector_collection trn_vector_collection_new_rag_setting_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trn_vector_collection
    ADD CONSTRAINT trn_vector_collection_new_rag_setting_id_fkey FOREIGN KEY (rag_setting_id) REFERENCES public.cfg_rag_setting(rag_setting_id);


--
-- PostgreSQL database dump complete
--

\unrestrict wNVyToERoDIahowuGxGgQLqqfDZ3xQ0ZuahAV4064jqJNN3a1Zf2VHew2Axdx0a

DROP TABLE IF EXISTS wf_sys_recfld_auto_tbl;

CREATE TABLE wf_sys_recfld_auto_tbl (
    business_unit   VARCHAR(30) NOT NULL DEFAULT '',
    record_id       VARCHAR(30) NOT NULL,
    field_id        VARCHAR(30) NOT NULL DEFAULT '',
    num_var         VARCHAR(50),
    first_reg_dtm   TIMESTAMP,
    first_reg_id    VARCHAR(50),
    last_update_dtm TIMESTAMP,
    last_update_id  VARCHAR(50),

    CONSTRAINT pk_wf_sys_recfld_auto_tbl
        PRIMARY KEY (business_unit, record_id, field_id)
);
