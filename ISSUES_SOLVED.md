# Issues Solved During Development

This document tracks major issues encountered and resolved during HackSheffield10.

## ✅ Issue #1: ConversationAgent suggests competitor retailers
**Status:** SOLVED  
**Commit:** b9c3231  
**Impact:** Critical - Frasers Group Challenge requirement

**Problem:** ConversationAgent suggested non-Frasers retailers (JD Sports, ASOS, Zalando, etc.)

**Solution:**
- Post-processing filter detecting 25+ competitor brands
- Replaces competitor mentions with Frasers-only response
- Applied to both Gemini and OpenAI paths

---

## ✅ Issue #2: Gemini safety filters blocking responses
**Status:** SOLVED  
**Commit:** b9c3231  
**Impact:** High - API reliability

**Problem:** Restrictive system instructions triggered Gemini safety filters (finish_reason=2)

**Solution:**
- Removed restrictive system instruction
- Implemented post-processing filter instead
- Allows natural generation, then filters output

---

## ✅ Issue #3: Image generation MIME type mismatch
**Status:** SOLVED  
**Impact:** High - Image display broken

**Problem:** Frontend used `image/jpeg` but backend generates PNG

**Solution:**
- Changed frontend to `image/png`
- Verified 1.6MB PNG images display correctly

---

## ✅ Issue #4: Agents not collaborating
**Status:** SOLVED  
**Impact:** Critical - Reply AI Agents Challenge requirement

**Problem:** Agents responded independently without context sharing

**Solution:**
- Increased history from 5 to 20 messages
- Pass full context to all agents
- Agents now build on each other's responses

---

## ✅ Issue #5: No Frasers product grounding
**Status:** SOLVED  
**Commit:** 8383cd8, ff94dbf  
**Impact:** High - Frasers Group Challenge requirement

**Problem:** Generic recommendations without real Frasers products

**Solution:**
- Google Search grounding with site: operators
- Restricted to Frasers domains only
- Real products with prices and links

---

## ✅ Issue #6: Missing observability
**Status:** SOLVED  
**Commit:** 01bba74  
**Impact:** Medium - Grafana Challenge requirement

**Problem:** No monitoring of multi-agent system

**Solution:**
- Prometheus metrics endpoint
- Grafana dashboard (4 panels)
- Real-time agent performance tracking

---

## ✅ Issue #7: Port conflicts and stale processes
**Status:** SOLVED  
**Impact:** Medium - Development workflow

**Problem:** Multiple API instances causing port conflicts

**Solution:**
- Proper process verification after kill commands
- Docker Compose for clean service management
- Removed orphan containers

---

## ✅ Issue #8: Python bytecode caching
**Status:** SOLVED  
**Impact:** Medium - Code updates not loading

**Problem:** __pycache__ preventing new code from running

**Solution:**
- Clear cache before each restart
- Added to deployment scripts

---

**Total Issues Solved:** 8  
**Development Time:** ~8 hours  
**All tests passing:** ✅
