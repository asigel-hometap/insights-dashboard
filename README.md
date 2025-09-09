# Insights Dashboard

A modern, responsive dashboard for managing Hometap's Smart Facts (Insights) content. Built for the Marketing team to track, filter, and export content management data.

## Features

- 📊 **Real-time Statistics** - Live counts of insights by status and type
- 🔍 **Advanced Filtering** - Search by ID, content, status, and type
- 👁️ **Dual Views** - Grid and list layouts for different use cases
- 📤 **CSV Export** - Download filtered data for spreadsheet analysis
- 🔄 **Auto-updates** - Automated data refresh from codebase
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Deployment with Vercel

### Quick Setup

1. **Fork this repository** or create a new one
2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Configure Environment Variables:**
   - `CODEBASE_PATH`: Path to your codebase (optional)
   - `GITHUB_TOKEN`: For automated updates (optional)

4. **Deploy:**
   - Vercel will automatically deploy
   - Your dashboard will be live at `https://your-project.vercel.app`

### Automated Updates

The dashboard automatically updates when:
- **Weekly**: Every Monday at 9 AM UTC
- **On Push**: When Smart Facts files change
- **Manual**: Trigger via GitHub Actions

### Manual Update

To manually update the dashboard:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the build script
python build_dashboard.py

# The script will generate index.html with fresh data
```

## Project Structure

```
insights-dashboard/
├── index.html                 # Generated dashboard (auto-created)
├── build_dashboard.py         # Data extraction script
├── requirements.txt           # Python dependencies
├── vercel.json               # Vercel configuration
├── .github/
│   └── workflows/
│       └── update-dashboard.yml
└── README.md
```

## Data Sources

The dashboard extracts data from:
- `eng_portals/portals/portals/apps/smart_facts/definitions.py`
- `eng_portals/portals/portals/apps/smart_facts/display_templates.py`

## Customization

### Adding New Status Types
Edit `build_dashboard.py` to add new status categories.

### Modifying the UI
Update the HTML template in `build_dashboard.py` to change the dashboard appearance.

### Changing Update Frequency
Modify the cron schedule in `.github/workflows/update-dashboard.yml`.

## Troubleshooting

### Dashboard not updating
- Check GitHub Actions logs
- Verify codebase path is correct
- Ensure Python dependencies are installed

### Missing data
- Verify Smart Facts files exist in the codebase
- Check file paths in `build_dashboard.py`
- Review extraction logic for errors

## Support

For issues or questions:
1. Check the GitHub Actions logs
2. Review the build script output
3. Verify Vercel deployment logs

## License

Internal use only - Hometap Smart Facts Dashboard
