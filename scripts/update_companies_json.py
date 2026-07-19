#!/usr/bin/env python3
"""
update_companies_json.py
Called by deploy-report.sh and deploy-profile.sh after each deployment.
Adds or updates a deliverable entry for a company in companies.json.

Usage:
    python3 update_companies_json.py <slug> <deliverable_type> <title> \
        <description> <url> <date> <companies_json_path>

deliverable_type: report | profile | ops
"""

import sys
import json
import os


def main():
    if len(sys.argv) < 8:
        print("Usage: update_companies_json.py <slug> <type> <title> <desc> <url> <date> <json_path>")
        sys.exit(1)

    slug = sys.argv[1]
    deliverable = sys.argv[2]   # report | profile | ops
    _title = sys.argv[3]   # unused but kept for call-site compat
    _description = sys.argv[4]   # unused but kept for call-site compat
    url = sys.argv[5]
    date = sys.argv[6]
    json_path = sys.argv[7]

    # Load existing data
    companies = []
    if os.path.exists(json_path):
        try:
            with open(json_path) as f:
                companies = json.load(f)
        except (json.JSONDecodeError, IOError):
            companies = []

    # Find or create the company entry
    entry = next((c for c in companies if c.get('slug') == slug), None)
    if entry is None:
        entry = {
            'slug':     slug,
            'name':     slug.replace('-', ' ').title(),
            'type_key': '',
            'type':     '',
            'location': '',
            'owner':    '',
            'founded':  None,
            'trucks':   None,
            'drivers':  None,
            'freight':  '',
            'tagline':  '',
            'pain_points': [],
            'report_url':  None,
            'profile_url': None,
            'ops_url':     None,
            'deployed':    date,
        }
        companies.append(entry)

    # Update the relevant URL field
    if deliverable == 'report':
        entry['report_url'] = url
    elif deliverable == 'profile':
        entry['profile_url'] = url
    elif deliverable == 'ops':
        entry['ops_url'] = url

    entry['deployed'] = date

    # Try to enrich from company_profile.md if it exists alongside the JSON
    # (VPS layout: /opt/carrier-factory/companies/{slug}/company_profile.md)
    agent_dir = os.path.dirname(os.path.dirname(
        json_path))  # /opt/carrier-factory/web -> /opt/carrier-factory
    profile_path = os.path.join(
        agent_dir, 'companies', slug, 'company_profile.md')
    if os.path.exists(profile_path):
        _enrich_from_profile(entry, profile_path)

    # Write back
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(companies, f, indent=2)

    print(f"companies.json updated: {slug} / {deliverable} -> {url}")


def _enrich_from_profile(entry, path):
    """Parse key fields from company_profile.md and update entry in-place."""
    try:
        with open(path) as f:
            text = f.read()
    except IOError:
        return

    import re

    def field(label):
        m = re.search(rf'\*\*{label}:\*\*\s*(.+)', text)
        return m.group(1).strip() if m else None

    if not entry.get('name') or entry['name'] == entry['slug'].replace('-', ' ').title():
        # First heading is the company name
        m = re.search(r'^#\s+(.+)', text, re.MULTILINE)
        if m:
            entry['name'] = m.group(1).strip()

    for src, dst in [('Type', 'type_key'), ('Location', 'location'),
                     ('Owner', 'owner'), ('Founded', 'founded'),
                     ('Primary Freight', 'freight'), ('Tagline', 'tagline')]:
        val = field(src)
        if val:
            if dst == 'founded':
                try:
                    entry[dst] = int(val)
                except ValueError:
                    entry[dst] = val
            else:
                entry[dst] = val

    # Fleet size: "38 trucks, 52 drivers"
    fs = field('Fleet Size')
    if fs:
        m = re.search(r'(\d+)\s+trucks?', fs)
        if m:
            entry['trucks'] = int(m.group(1))
        m = re.search(r'(\d+)\s+drivers?', fs)
        if m:
            entry['drivers'] = int(m.group(1))

    # Map type_key to display label
    type_map = {
        'owner_operator':   'Owner-Operator',
        'small_fleet':      'Small Fleet',
        'regional_carrier': 'Regional Carrier',
        'mid_size_carrier': 'Mid-Size Carrier',
    }
    tk = entry.get('type_key', '').lower().replace(' ', '_')
    entry['type'] = type_map.get(tk, entry.get('type_key', ''))
    entry['type_key'] = tk


if __name__ == '__main__':
    main()
