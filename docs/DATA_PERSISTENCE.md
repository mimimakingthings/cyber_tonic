# Data Persistence Documentation

## Overview

The Cyber Tonic Client Portal now includes comprehensive data persistence functionality that automatically saves and loads client data and assessment data between sessions. This ensures that your work is never lost and you can continue where you left off.

## Features

### Automatic Data Persistence
- **Auto-save on changes**: Data is automatically saved when you add clients or update assessments
- **Auto-load on startup**: All saved data is automatically loaded when you start the application
- **Change detection**: The system detects when data has changed and saves accordingly

### Data Storage
- **JSON file storage**: All data is stored in human-readable JSON format
- **Structured storage**: Data is organized in separate files for clients, assessments, and evidence files
- **Backup system**: Automatic backups are created before each save operation
- **Metadata tracking**: Each data file includes metadata about when it was last updated

### Manual Data Management
- **Manual save**: "Save All Data" button in the sidebar for manual saving
- **Storage information**: View storage details and file information
- **Export functionality**: Export all data or specific data types
- **Last save indicator**: Shows when data was last saved

## Storage Location

Data is stored in the `data/storage/` directory with the following structure:

```
data/storage/
├── clients.json          # Client information
├── assessments.json      # Assessment data by client
├── evidence_files.json   # Evidence file references
└── backups/             # Automatic backups
    ├── clients_backup_YYYYMMDD_HHMMSS.json
    ├── assessments_backup_YYYYMMDD_HHMMSS.json
    └── evidence_files_backup_YYYYMMDD_HHMMSS.json
```

## Data Format

### Clients Data
```json
{
  "clients": [
    {
      "id": "unique-client-id",
      "name": "Client Name",
      "industry": "Industry Type",
      "contact": {
        "email": "email@example.com",
        "phone": "phone-number",
        "primary": "Primary Contact Name"
      },
      "size": "Company Size",
      "documents": ["document1.pdf", "document2.docx"],
      "notes": "Client notes",
      "created_date": "2025-10-17T09:23:23.062187"
    }
  ],
  "metadata": {
    "last_updated": "2025-10-17T09:23:23.062187",
    "total_clients": 1,
    "version": "1.0"
  }
}
```

### Assessments Data
```json
{
  "assessments": {
    "client-id": {
      "GV.OC-01": {
        "status": "Fully Implemented",
        "score": 8,
        "notes": "Assessment notes",
        "evidence": ["evidence1.pdf"]
      }
    }
  },
  "metadata": {
    "last_updated": "2025-10-17T09:23:23.062187",
    "total_clients": 1,
    "version": "1.0"
  }
}
```

## Usage

### Automatic Features
1. **Start the application**: Data is automatically loaded from storage
2. **Add a client**: Client data is automatically saved
3. **Update assessments**: Assessment data is automatically saved
4. **Close and reopen**: All data is preserved and loaded automatically

### Manual Features
1. **Manual Save**: Click "💾 Save All Data" in the sidebar
2. **Storage Info**: Click "📊 Storage Info" to view storage details
3. **Export Data**: Use the export buttons to download data
4. **Last Save Time**: View when data was last saved in the sidebar

## Backup System

- **Automatic backups**: Created before each save operation
- **Backup retention**: Keeps the 10 most recent backups
- **Backup naming**: `{data_type}_backup_YYYYMMDD_HHMMSS.json`
- **Recovery**: Manual recovery from backup files if needed

## Export/Import

### Export Options
- **Complete Export**: All data (clients, assessments, evidence files)
- **Clients Only**: Just client information
- **Assessments Only**: Just assessment data

### Export Format
Exports include:
- All current data
- Export metadata (date, version, source)
- Timestamped filename

## Error Handling

- **Graceful degradation**: If data loading fails, the application starts with empty data
- **Error logging**: All errors are logged for debugging
- **User feedback**: Clear success/error messages for all operations
- **Backup protection**: Backups are created before any save operation

## Security Considerations

- **Local storage**: Data is stored locally on your machine
- **No encryption**: Data is stored in plain JSON format
- **File permissions**: Respects system file permissions
- **Backup security**: Backups are stored in the same directory structure

## Troubleshooting

### Data Not Loading
1. Check if storage directory exists: `data/storage/`
2. Verify file permissions
3. Check application logs for error messages
4. Try manual save to test write permissions

### Data Not Saving
1. Check available disk space
2. Verify write permissions to storage directory
3. Check application logs for error messages
4. Try manual save button

### Corrupted Data
1. Check backup files in `data/storage/backups/`
2. Restore from most recent backup
3. Contact support if backups are also corrupted

## Technical Details

### Dependencies
- `json`: Standard library for JSON handling
- `pathlib`: Modern path handling
- `datetime`: Timestamp generation
- `logging`: Error logging and debugging

### Performance
- **Fast loading**: JSON files load quickly even with large datasets
- **Efficient saving**: Only saves when data actually changes
- **Minimal overhead**: Lightweight implementation with minimal performance impact

### Scalability
- **File-based storage**: Suitable for small to medium datasets
- **JSON format**: Human-readable and easily portable
- **Modular design**: Easy to extend or replace storage backend

## Future Enhancements

Potential improvements for future versions:
- Database integration (SQLite, PostgreSQL)
- Data encryption for sensitive information
- Cloud storage integration
- Data synchronization across devices
- Advanced backup and recovery options
- Data validation and integrity checks
