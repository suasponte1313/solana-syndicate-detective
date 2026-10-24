#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.parse
from core.investigator import INVESTIGATOR

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "settings.json")

class SupabaseBridge:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f).get("supabase", {})
        except Exception:
            return {}

    def export_sql_migration(self) -> str:
        """Generates 1-Click PostgreSQL DDL for Supabase"""
        sql = """-- ==============================================================================
-- 🕵️ SOLANA SYNDICATE DETECTIVE — SUPABASE EVIDENCE VAULT SCHEMA
-- ==============================================================================

CREATE TABLE IF NOT EXISTS public.syndicates (
    syndicate_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mastermind_vault TEXT NOT NULL,
    threat_level TEXT NOT NULL,
    total_extracted_sol NUMERIC DEFAULT 0,
    member_count INTEGER DEFAULT 0,
    datacenter_location TEXT,
    primary_mo TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.suspects (
    address TEXT PRIMARY KEY,
    alias TEXT NOT NULL,
    syndicate_id TEXT REFERENCES public.syndicates(syndicate_id),
    tier TEXT DEFAULT 'TIER_1',
    win_rate NUMERIC DEFAULT 0,
    extracted_sol NUMERIC DEFAULT 0,
    total_txs INTEGER DEFAULT 0,
    copy_bot_count INTEGER DEFAULT 0,
    genesis_parent TEXT NOT NULL,
    threat_level TEXT DEFAULT 'HIGH',
    play_style TEXT,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for instant sub-millisecond detective lookups
CREATE INDEX IF NOT EXISTS idx_suspects_syndicate ON public.suspects(syndicate_id);
CREATE INDEX IF NOT EXISTS idx_suspects_genesis ON public.suspects(genesis_parent);
CREATE INDEX IF NOT EXISTS idx_suspects_win_rate ON public.suspects(win_rate DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE public.syndicates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.suspects ENABLE ROW LEVEL SECURITY;

-- Allow read access to authenticated and anonymous analysts
CREATE POLICY "Public read syndicate evidence" ON public.syndicates FOR SELECT USING (true);
CREATE POLICY "Public read suspect files" ON public.suspects FOR SELECT USING (true);
"""
        return sql

    def sync_to_supabase(self):
        """Attempts sync to configured Supabase project or generates payload"""
        url = self.config.get("url")
        key = self.config.get("api_key")
        data = INVESTIGATOR.get_crime_board_data()

        if not url or not key or "placeholder" in url:
            return {
                "status": "LOCAL_ONLY",
                "message": "Supabase credentials pending in config/settings.json. SQL Migration generated.",
                "sql_ddl": self.export_sql_migration(),
                "payload_size": len(data.get("top_wanted", []))
            }

        try:
            # Upsert syndicates
            headers = {
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            req = urllib.request.Request(
                f"{url}/rest/v1/syndicates",
                headers=headers,
                data=json.dumps(data["syndicates"]).encode("utf-8"),
                method="POST"
            )
            urllib.request.urlopen(req, timeout=5)
            return {"status": "SUCCESS", "synced_syndicates": len(data["syndicates"])}
        except Exception as e:
            return {"status": "ERROR", "error": str(e), "sql_ddl": self.export_sql_migration()}

BRIDGE = SupabaseBridge()
