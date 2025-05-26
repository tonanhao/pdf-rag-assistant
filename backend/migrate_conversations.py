#!/usr/bin/env python3
"""
Migration script to add user_id to existing conversations.
This script assigns existing conversations to a default user or prompts for assignment.
"""

import json
import os
from pathlib import Path
import sys

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.config import CONVERSATION_DIR

def migrate_conversations():
    """
    Migrate existing conversations to include user_id
    """
    print("🔄 Starting conversation migration...")
    
    # Get all conversation files
    conversation_files = list(CONVERSATION_DIR.glob("*.json"))
    
    if not conversation_files:
        print("📭 No conversation files found.")
        return
    
    print(f"📁 Found {len(conversation_files)} conversation files")
    
    # Ask for default user ID
    print("\n❓ How would you like to handle existing conversations?")
    print("1. Assign all to a specific user ID")
    print("2. Delete all (they will be recreated per user)")
    print("3. Cancel migration")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        user_id = input("Enter the user ID to assign conversations to: ").strip()
        if not user_id:
            print("❌ Invalid user ID. Migration cancelled.")
            return
        
        migrate_to_user(conversation_files, user_id)
        
    elif choice == "2":
        confirm = input("⚠️  Are you sure you want to delete all conversations? (yes/no): ").strip().lower()
        if confirm == "yes":
            delete_all_conversations(conversation_files)
        else:
            print("❌ Migration cancelled.")
            
    elif choice == "3":
        print("❌ Migration cancelled.")
        
    else:
        print("❌ Invalid choice. Migration cancelled.")

def migrate_to_user(conversation_files, user_id):
    """
    Assign all conversations to a specific user
    """
    print(f"🔄 Assigning {len(conversation_files)} conversations to user {user_id}...")
    
    migrated_count = 0
    
    for file_path in conversation_files:
        try:
            # Load conversation
            with open(file_path, 'r') as f:
                conversation = json.load(f)
            
            # Add user_id if not present
            if 'user_id' not in conversation:
                conversation['user_id'] = user_id
                
                # Save back to file
                with open(file_path, 'w') as f:
                    json.dump(conversation, f)
                
                migrated_count += 1
                print(f"✅ Migrated {file_path.name}")
            else:
                print(f"⏭️  Skipped {file_path.name} (already has user_id)")
                
        except Exception as e:
            print(f"❌ Error migrating {file_path.name}: {e}")
    
    print(f"🎉 Migration completed! {migrated_count} conversations migrated.")

def delete_all_conversations(conversation_files):
    """
    Delete all existing conversations
    """
    print(f"🗑️  Deleting {len(conversation_files)} conversations...")
    
    deleted_count = 0
    
    for file_path in conversation_files:
        try:
            file_path.unlink()
            deleted_count += 1
            print(f"🗑️  Deleted {file_path.name}")
        except Exception as e:
            print(f"❌ Error deleting {file_path.name}: {e}")
    
    print(f"🎉 Cleanup completed! {deleted_count} conversations deleted.")

if __name__ == "__main__":
    migrate_conversations() 