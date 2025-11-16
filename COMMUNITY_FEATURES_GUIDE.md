# Community Features - Quick Start Guide

## 🚀 Quick Navigation

### URLs
- **View All Communities**: `/confessions/communities/`
- **Create Community**: `/confessions/communities/create/` (login required)
- **View Community**: `/confessions/communities/<id>/`
- **Delete Community**: `/confessions/communities/<id>/delete/` (creator only)

## 📋 Feature Overview

### 1. Community List
**URL**: `/confessions/communities/`
**What you see**:
- Grid of all communities
- Community name, description, creator
- Confession count and creation date
- "View Community" button
- "Delete" button (if you're the creator)

**How to use**:
1. Navigate to Communities from the sidebar
2. Browse all communities
3. Click a community card to view details

### 2. Create Community
**URL**: `/confessions/communities/create/`
**Requirements**: Must be logged in
**Form fields**:
- Community Name (required)
- Description (required)

**How to create**:
1. Click "Create Community" button (from Communities page or sidebar)
2. Fill in community name and description
3. Click "Create Community"
4. You'll be redirected to your new community's detail page

### 3. Community Details
**URL**: `/confessions/communities/<id>/`
**What you see**:
- Large community header with gradient background
- Community statistics (confessions count, creation date, creator)
- List of all confessions in this community
- Comments for each confession (first 3 shown, count displayed)
- Sidebar with community info

**Special features**:
- Click on community name in any confession to jump to that community
- Delete button only appears if you created the community
- Comments display with author names (or "Anonymous" for unauthenticated users)

### 4. Delete Community
**URL**: `/confessions/communities/<id>/delete/`
**Requirements**: Must be logged in AND be the community creator
**Process**:
1. Go to your community's detail page
2. Click "Delete Community" button (red button, only for creator)
3. Review the confirmation page with all community details
4. Click "Yes, Delete Community" to confirm
5. You'll be redirected to the community list
6. The community and all its confessions will be permanently deleted

## 👥 User Permissions

### Anonymous Users (Not Logged In)
- ✅ View all communities
- ✅ View community details
- ✅ View confessions and comments
- ❌ Cannot create communities
- ❌ Cannot delete communities

### Logged-In Users
- ✅ View all communities
- ✅ View community details
- ✅ Create new communities
- ✅ Delete their own communities
- ❌ Cannot delete other users' communities

## 🎯 Common Tasks

### Task: Find a Community
1. Go to `/confessions/communities/`
2. Browse the list OR use browser search (Ctrl+F) to search
3. Click the community card to view details

### Task: Create a Community for Your Interest
1. Log in to your account
2. Click "Communities" in navigation
3. Click "Create Community" button
4. Fill in a name and description
5. Click "Create Community"
6. You're now the creator of your community!

### Task: Post a Confession to a Specific Community
Currently: Confessions are posted globally. Future feature to link confessions to communities during creation.

### Task: See All Confessions in a Community
1. Navigate to the community detail page
2. Scroll through the list of confessions
3. Click on any confession to see all comments
4. Click "Summarize" to get AI summary of comments

### Task: Delete Your Community
1. Go to your community detail page
2. Click the red "Delete Community" button
3. Confirm the deletion
4. Your community is permanently deleted

## 🔐 Security Notes

- **Logged-in only**: Only authenticated users can create/delete communities
- **Creator only**: Only the person who created a community can delete it
- **No spam**: Each community name is unique
- **Data protection**: All forms include CSRF protection
- **Cascade delete**: Deleting a community deletes all its confessions

## 🎨 Template Structure

### Community List Template
```
Header Section
├─ Title & Description
├─ Create Community button (if logged in)
└─ Community Grid
   ├─ Community Card (repeating)
   │  ├─ Community Name
   │  ├─ Creator Name
   │  ├─ Description
   │  ├─ Statistics
   │  └─ Action Buttons
   └─ Empty State (if no communities)
```

### Community Detail Template
```
Community Header (Gradient)
├─ Community Name
├─ Description
├─ Statistics
└─ Delete Button (if creator)

Two-Column Layout
├─ Main Column
│  └─ Confessions List
│     ├─ Confession 1
│     │  ├─ Content
│     │  ├─ Meta (author, date, upvotes)
│     │  └─ Comments
│     ├─ Confession 2
│     └─ ... More Confessions
└─ Sidebar
   ├─ About Section
   │  ├─ Creator Name
   │  ├─ Creation Date
   │  └─ Confession Count
   └─ Back Button
```

## 📊 Database Schema

### Community Model
```python
Community
├─ id (Primary Key)
├─ name (CharField, unique)
├─ description (TextField)
├─ created_by (ForeignKey to User)
├─ created_at (DateTime)
└─ updated_at (DateTime)
```

### Confession Model (Updated)
```python
Confession
├─ id (Primary Key)
├─ content (TextField)
├─ created_at (DateTime)
├─ upvotes (Integer)
├─ author (ForeignKey to User, nullable)
└─ community (ForeignKey to Community, nullable, CASCADE)
    └─ related_name='confessions'
```

## 🚨 Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "You do not have permission to delete this community" | You're trying to delete someone else's community | Only the creator can delete |
| Redirected to login page | You tried to create/delete community without login | Log in first |
| "Community not found" (404) | Community doesn't exist or was deleted | Check the URL or browse communities |

## 📱 Responsive Design

- Desktop (> 1024px): Two-column layout (confessions + sidebar)
- Tablet (768px - 1024px): Single column with sidebar below
- Mobile (< 768px): Single column, sidebar at bottom
- All buttons and links work on touch devices

## 🔧 Developer Notes

### View Decorators
```python
@login_required  # Applied to community_create and community_delete
def your_view(request):
    pass
```

### Permission Check Pattern
```python
if community.created_by != request.user:
    messages.error(request, 'Permission denied')
    return redirect('community_detail', pk=community.pk)
```

### Query Patterns
```python
# Get all confessions in a community
confessions = community.confessions.all()

# Get confessions without community
confessions = Confession.objects.filter(community__isnull=True)

# Get communities created by a user
communities = Community.objects.filter(created_by=request.user)
```

## 📝 Notes

- Communities are created with the current user as `created_by`
- Each community name must be unique
- Descriptions support plain text (no HTML tags)
- Deleting a community cascades to delete all its confessions
- Confessions can exist without a community
- The community_list view doesn't require authentication

---

**Last Updated**: November 16, 2025
**Version**: 1.0
