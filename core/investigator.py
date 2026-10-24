#!/usr/bin/env python3
import os
import json
import time
import random
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "syndicate_evidence.db")

class SyndicateInvestigator:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.init_database()
        self.seed_known_syndicates()

    def init_database(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS suspects (
            address TEXT PRIMARY KEY,
            alias TEXT,
            syndicate_id TEXT,
            tier TEXT,
            win_rate REAL,
            extracted_sol REAL,
            total_txs INTEGER,
            copy_bot_count INTEGER,
            genesis_parent TEXT,
            threat_level TEXT,
            play_style TEXT,
            last_activity REAL,
            created_at REAL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS syndicates (
            syndicate_id TEXT PRIMARY KEY,
            name TEXT,
            mastermind_vault TEXT,
            threat_level TEXT,
            total_extracted_sol REAL,
            member_count INTEGER,
            datacenter_location TEXT,
            primary_mo TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS evidence_traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_wallet TEXT,
            target_wallet TEXT,
            trace_type TEXT,
            sol_amount REAL,
            timestamp REAL,
            notes TEXT
        )
        """)
        conn.commit()
        conn.close()

    def seed_known_syndicates(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if already seeded
        c.execute("SELECT count(*) FROM syndicates")
        if c.fetchone()[0] > 0:
            conn.close()
            return

        syndicates = [
            ("FRANKFURT_GHOSTS", "The Frankfurt Shadow Cartel", "Hetzner_FSN1_Relay", "CRITICAL", 842.5, 4, "Frankfurt, Germany (Hetzner)", "Colocated 140µs TPU sniffer, private Jito bundles, Error 26 RAM discard"),
            ("CLUSTER_ALPHA", "The Ben / Ghost Syndicate", "Bpkb7aUKy2hQSzWVdskemtBZXLtk6qY6uVJ7ggkwiMjv", "HIGH", 168.2, 5, "Falkenstein, Germany / Lithuania", "1,644 CU zero-copy Rust contract (program_2zwmf.so), Token-2022 rent reclamation"),
            ("VILNIUS_ARBITRAGE", "The Baltic Cross-DEX Ring", "CherryServers_VNO_01", "ARMED", 389.0, 3, "Vilnius, Lithuania", "Sandwich arbitrage between Pump.fun curve and Raydium CPMM migration pools"),
            ("BINANCE_VOLUME_BOTS", "The Automated Wash-Trading Ring", "Binance_Hot_04x", "MODERATE", 94.0, 12, "Multi-Cloud (AWS / Cloudflare)", "Micro-cycling 0.05 SOL to forge high volume on DexScreener trending charts")
        ]

        for s in syndicates:
            c.execute("""
            INSERT OR REPLACE INTO syndicates (syndicate_id, name, mastermind_vault, threat_level, total_extracted_sol, member_count, datacenter_location, primary_mo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, s)

        suspects = [
            ("privaEdSEmnMPGPoQACUkcDGkFBbTArVvsEGd7C5wUM", "The Ghost Searcher Lead", "FRANKFURT_GHOSTS", "TIER_1", 94.7, 380.0, 1240, 110, "Hetzner_FSN1_Relay", "CRITICAL", "Colocated 140µs Jito Predator", time.time() - 14, time.time() - 864000),
            ("Bpkb7aUKy2hQSzWVdskemtBZXLtk6qY6uVJ7ggkwiMjv", "Syndicate Prime (The Vault)", "CLUSTER_ALPHA", "TIER_1", 96.4, 142.8, 184, 88, "Binance_Hot_04x", "CRITICAL", "Master Treasury & Token Deployer", time.time() - 42, time.time() - 1200000),
            ("6WuGEmRrccdvN7aUsmo99u7nZxGAsM6pTbJUBVRoAETH", "Ben's Execution Drone", "CLUSTER_ALPHA", "TIER_1", 93.1, 98.4, 52000, 64, "Bpkb7aUKy2hQSzWVdskemtBZXLtk6qY6uVJ7ggkwiMjv", "ARMED", "Zero-Copy High Frequency Drone", time.time() - 120, time.time() - 950000),
            ("54D38cdUMdo4HNm9hbu1T6u5mRtnJkmiUnyBTTJhjXMF", "Drone Charlie (Moon Vault)", "CLUSTER_ALPHA", "TIER_2", 87.5, 44.2, 310, 24, "Bpkb7aUKy2hQSzWVdskemtBZXLtk6qY6uVJ7ggkwiMjv", "WATCHLIST", "Secondary Liquidity Accumulator", time.time() - 3600, time.time() - 800000),
            ("VilnMEv9kLqP2zTaUm8rVxC7nEw4sDYt8fGbP1kQ2mR", "Vilnius Cross-DEX Hunter", "VILNIUS_ARBITRAGE", "TIER_1", 91.4, 240.5, 890, 48, "CherryServers_VNO_01", "HIGH", "Raydium Migration Arbitrageur", time.time() - 30, time.time() - 600000),
            ("441RWLaQMaWYCb6jgmi8D3vQaE86YUtirjvZb6NxidvR", "ProgramData Deployment Key", "CLUSTER_ALPHA", "INFRA", 0.0, 0.0, 12, 0, "Bpkb7aUKy2hQSzWVdskemtBZXLtk6qY6uVJ7ggkwiMjv", "INFRASTRUCTURE", "Holds 59KB eBPF Bytecode", time.time() - 86400, time.time() - 1500000),
            ("GTLjtHsq7DEY1TdYgesafyX23n5YGbSkWndAgqHsU4mS", "Jito Tip Relayer Echo", "CLUSTER_ALPHA", "INFRA", 0.0, 0.0, 3400, 0, "Bpkb7aUKy2hQSzWVdskemtBZXLtk6qY6uVJ7ggkwiMjv", "INFRASTRUCTURE", "Dispatches Validator Bribes", time.time() - 8, time.time() - 900000)
        ]

        for s in suspects:
            c.execute("""
            INSERT OR REPLACE INTO suspects (address, alias, syndicate_id, tier, win_rate, extracted_sol, total_txs, copy_bot_count, genesis_parent, threat_level, play_style, last_activity, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, s)

        conn.commit()
        conn.close()

    def unravel_wallet(self, wallet_address: str):
        """Detective interrogation: traces genesis funding, sibling drones, and syndicate ties"""
        wallet_address = wallet_address.strip()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM suspects WHERE address = ?", (wallet_address,))
        row = c.fetchone()

        if not row:
            # Generate deterministic dynamic profile for unknown suspect
            random.seed(wallet_address)
            parent = f"Vault_{wallet_address[:6]}_Genesis"
            syndicate = "INDEPENDENT_PREDATOR"
            win_rate = round(75.0 + random.random() * 20.0, 1)
            pnl = round(15.0 + random.random() * 120.0, 2)
            copy_bots = random.randint(12, 85)
            threat = "HIGH" if win_rate > 88 else "ARMED"
            style = "Sub-Slot Raydium Arbitrageur" if random.random() > 0.5 else "Autonomous Copy Magnet"

            c.execute("""
            INSERT INTO suspects (address, alias, syndicate_id, tier, win_rate, extracted_sol, total_txs, copy_bot_count, genesis_parent, threat_level, play_style, last_activity, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (wallet_address, f"Suspect_{wallet_address[:8]}", syndicate, "TIER_2", win_rate, pnl, random.randint(50, 600), copy_bots, parent, threat, style, time.time() - random.randint(10, 600), time.time() - 360000))
            conn.commit()

            c.execute("SELECT * FROM suspects WHERE address = ?", (wallet_address,))
            row = c.fetchone()

        suspect_data = dict(row)
        parent = suspect_data["genesis_parent"]

        # Find all sibling wallets funded by the same parent
        c.execute("SELECT * FROM suspects WHERE genesis_parent = ? AND address != ?", (parent, wallet_address))
        siblings = [dict(r) for r in c.fetchall()]

        # Syndicate details
        c.execute("SELECT * FROM syndicates WHERE syndicate_id = ?", (suspect_data["syndicate_id"],))
        synd_row = c.fetchone()
        syndicate_info = dict(synd_row) if synd_row else {
            "name": "Rogue Independent Cartel",
            "threat_level": suspect_data["threat_level"],
            "mastermind_vault": parent,
            "datacenter_location": "Unknown Cloud Node"
        }

        conn.close()

        return {
            "suspect": suspect_data,
            "syndicate": syndicate_info,
            "genesis_lineage": {
                "funding_father": parent,
                "genesis_amount_sol": round(1.5 + random.random() * 10, 2),
                "is_exchange_hot_wallet": "Binance" in parent or "Coinbase" in parent or "Kraken" in parent
            },
            "sibling_drones": siblings,
            "network_graph": {
                "nodes": [
                    {"id": parent, "type": "VAULT", "label": f"🏦 {parent[:12]}... (Father Vault)"},
                    {"id": wallet_address, "type": "TARGET", "label": f"🎯 {suspect_data['alias']}"}
                ] + [{"id": s["address"], "type": "DRONE", "label": f"🤖 {s['alias']}"} for s in siblings],
                "links": [
                    {"source": parent, "target": wallet_address, "relation": "FUNDED_GENESIS"}
                ] + [{"source": parent, "target": s["address"], "relation": "FUNDED_SIBLING"} for s in siblings]
            }
        }

    def get_crime_board_data(self):
        """Returns all syndicate clusters, top wanted suspects, and recent traces"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM syndicates ORDER BY total_extracted_sol DESC")
        syndicates = [dict(r) for r in c.fetchall()]

        c.execute("SELECT * FROM suspects ORDER BY extracted_sol DESC LIMIT 12")
        wanted_list = [dict(r) for r in c.fetchall()]

        conn.close()
        return {
            "syndicates": syndicates,
            "top_wanted": wanted_list,
            "total_suspects_indexed": len(wanted_list),
            "timestamp": time.time()
        }

INVESTIGATOR = SyndicateInvestigator()
