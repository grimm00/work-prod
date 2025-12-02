# Projects Feature - Phase 6: GitHub Integration

**Phase:** 6 - GitHub Metadata Synchronization  
**Duration:** 2 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 5 complete

---

## 📋 Overview

Phase 6 adds GitHub integration to automatically sync repository metadata (description, stars, languages, last_updated) for projects with a `remote_url` pointing to GitHub. This keeps project information current without manual updates.

**Success Definition:** Can click "Sync" on a project and see updated GitHub metadata.

---

## 🎯 Goals

1. **GitHub API Client** - Fetch repo metadata from GitHub
2. **POST /api/projects/{id}/sync** - Sync endpoint
3. **Sync UI** - Sync button on project detail
4. **Rate Limit Handling** - Respect GitHub API rate limits
5. **Error Handling** - Handle private repos, 404s gracefully

---

## 📝 TDD Tasks

### Backend GitHub Integration

- [ ] Write GitHub sync tests
  - Test fetching public repo metadata
  - Test updating project with GitHub data
  - Test rate limit handling
  - Test error handling (404, private repo)
- [ ] Create GitHub API client
  - Fetch description, stars, last_updated, languages
  - Parse GitHub URL
  - Handle authentication (optional token)
  - Respect rate limits (cache results)
- [ ] Implement POST /api/projects/{id}/sync
  - Validate project has remote_url
  - Parse GitHub owner/repo from URL
  - Fetch metadata
  - Update project record
  - Store `last_synced` timestamp

### Frontend Sync UI

- [ ] Write sync UI tests
- [ ] Add sync button to ProjectDetail component
- [ ] Show last_synced timestamp
- [ ] Show sync status (loading/success/error)
- [ ] Add Zustand `syncProject()` action

### Batch Sync (Optional)

- [ ] Implement batch sync for multiple projects
- [ ] Background sync job (future enhancement)

### Manual Testing

- [ ] Sync GitHub project
- [ ] Verify metadata updates
- [ ] Test error handling (invalid URL, private repo)
- [ ] Verify rate limit handling

---

## ✅ Completion Criteria

- [ ] GitHub API client working
- [ ] Sync endpoint updates projects
- [ ] Sync button in UI working
- [ ] Last synced timestamp displayed
- [ ] Error handling for edge cases
- [ ] Rate limit awareness
- [ ] All tests passing

---

## 📦 Deliverables

- GitHub API client
- POST /api/projects/{id}/sync endpoint
- Sync button UI
- Last synced display
- Backend and frontend tests

---

## 🔗 Dependencies

**Prerequisites:** Phase 5 complete  
**Blocks:** Phase 7  
**External:** GitHub API (public, unauthenticated access)

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started

