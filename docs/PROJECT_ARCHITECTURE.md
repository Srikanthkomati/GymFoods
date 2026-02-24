# GymFoods Personal Assistant - Architecture & Start Plan

## 1) Product goal
Build a personal assistant that gives:
- Daily workout reminders
- Seasonal diet suggestions (winter/summer/monsoon, etc.)
- Goal-based nutrition guidance (healthy weight gain or weight loss)
- Affordable, locally relevant meal suggestions
- User-specific plans based on onboarding profile and food preference for the day

## 2) Recommended MVP scope (first 50 users)
### Core features
1. User onboarding
   - Name, age, gender (optional), height, weight
   - Fitness goal: weight gain / weight loss / maintenance
   - Activity level, workout days, dietary preference (veg/non-veg/eggetarian)
   - Budget level (low/medium/high)
   - Allergies and food restrictions
   - City/location (or GPS permission)
2. Daily plan generation
   - Workout card for the day
   - Meal plan for breakfast/lunch/snacks/dinner
   - Seasonal and local ingredient preference
   - "What do I feel like eating?" input (e.g., spicy, light, rice-based, high-protein)
3. Reminder system
   - Morning plan reminder
   - Meal-time reminders
   - Evening hydration/protein reminder
4. Progress tracking
   - Daily check-in: followed/not followed
   - Weekly weight trend

### Non-goals for MVP
- Real-time wearable integrations
- Advanced AI personalization from large history
- Multi-language voice assistant

## 3) Suggested architecture
Use a simple modular monolith first (faster for one laptop server and 50 users).

### High-level components
1. Frontend (Web app)
   - React + Next.js
   - Pages: onboarding, dashboard, today plan, profile
2. Backend API
   - Node.js + NestJS (or Express if you prefer minimal setup)
   - Modules:
     - Auth module
     - User profile module
     - Plan generation module
     - Seasonal-food module
     - Reminder scheduler module
3. Database
   - PostgreSQL
   - Tables for users, profiles, goals, food preferences, plans, reminders, check-ins
4. Background scheduler
   - Cron-based worker (node-cron / BullMQ)
   - Generates next-day plans and sends reminders
5. Notification service
   - Email first (free tier)
   - Optional: WhatsApp/SMS later

### Why this works for your setup
- Easy to run on a laptop with Docker
- Easy to deploy later to cloud VPS
- Can scale from 50 users to a few thousand by separating worker + DB

## 4) Data model (MVP)
- users(id, name, email, password_hash, created_at)
- profiles(user_id, age, height_cm, weight_kg, goal, activity_level, city, diet_type, budget_tier)
- restrictions(user_id, allergies_json, avoid_foods_json)
- preferences(user_id, taste_tags_json)
- daily_plans(id, user_id, date, workout_json, meals_json, calories_target, protein_target)
- checkins(id, user_id, date, weight_kg, adherence_score, notes)
- reminders(id, user_id, reminder_type, schedule_time, channel, enabled)

## 5) Seasonal + local diet strategy
1. Determine season from location + date
   - Start with rule-based mapping by city/country + month
2. Build ingredient catalog
   - seasonal_ingredients table by region + season + average price category
3. Meal recommendation logic (first version)
   - Filter by goal (gain/loss)
   - Filter by allergies/restrictions
   - Filter by user taste choice ("what I feel like")
   - Rank by nutrition score + affordability + availability
4. Later upgrade
   - Add local market APIs when needed

## 6) Plan generation logic (simple and strong)
Use a scoring pipeline:
- nutrition_match_score (goal alignment)
- taste_match_score (user mood input)
- seasonality_score (ingredient in season)
- affordability_score (budget match)
- variety_penalty (avoid same meals every day)

Final score = weighted sum. Pick top meals.

## 7) Tech stack recommendation
- Frontend: Next.js + Tailwind
- Backend: NestJS + TypeScript
- DB: PostgreSQL + Prisma ORM
- Jobs: BullMQ + Redis (or node-cron in v1)
- Auth: JWT with refresh token
- Infra: Docker Compose on your laptop server
- Monitoring: Uptime Kuma + basic logs

## 8) Security and reliability basics
- Store hashed passwords (bcrypt/argon2)
- Use HTTPS (Caddy/Nginx reverse proxy + Let's Encrypt)
- Daily DB backup (cron job to compressed dump)
- Separate .env secrets from repo
- Add rate limiting on auth endpoints

## 9) Development workflow (as requested)
Branching strategy:
- main: production-ready
- development: integration branch
- feature/*: each new feature

Per change:
1. Create feature branch from development
2. Implement + test locally
3. Open PR to development
4. Review checklist
5. Merge after approval

Suggested PR checklist:
- Feature works as expected
- No hardcoded secrets
- DB migrations included
- Basic tests pass
- API contract documented

## 10) 4-week build plan
### Week 1
- Project setup (frontend + backend + DB + Docker)
- Auth + onboarding forms
- Store user profile and goal

### Week 2
- Seasonal ingredient dataset (manual CSV seed)
- Rule-based diet generator
- Daily plan API and dashboard UI

### Week 3
- Reminder scheduler
- Email reminders
- Daily check-in and progress tracking

### Week 4
- Improve recommendation scoring
- Add budget-aware filtering
- Test with 5-10 pilot users
- Stabilize and prepare deployment docs

## 11) Deploying on your always-on laptop
Minimum:
- 16 GB RAM preferred
- Stable internet + static IP or dynamic DNS
- Docker + Docker Compose
- Reverse proxy + HTTPS

Important:
- Keep automated backups to external drive/cloud storage
- Use UPS power backup if possible
- Monitor CPU/RAM and restart policies

## 12) What you may be missing (important additions)
- Legal/privacy page because you store health-related info
- Data retention policy (delete inactive users after X months)
- "Not medical advice" disclaimer in app
- Admin page for manually correcting meal catalog data
- Feedback loop: "Did you like this meal?" to improve recommendations

## 13) First implementation tasks (actionable)
1. Initialize monorepo with `apps/web` and `apps/api`
2. Add Docker Compose for web, api, postgres
3. Build onboarding API + UI
4. Create seed data for seasonal ingredients
5. Implement first daily plan endpoint
6. Build dashboard to show today's workout + meals
7. Add one daily reminder job

This plan gives a practical, low-cost path from idea to usable product for the first 50 users while staying easy to scale later.
