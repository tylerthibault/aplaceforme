#!/usr/bin/env python3
"""
Seed file to populate the database with sample data.
This script adds 5 items to each table for development and testing purposes.
"""

import sys
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

from src import create_app, db
from src.models import (
    User, BlogPost, GodStory, Song, Testimonial, 
    Subscriber, Newsletter, RadioSession, SessionToken, LogEntry
)
import config

def create_sample_users():
    """Create sample users including admin and regular users."""
    users = [
        {
            'username': 'admin',
            'email': 'admin@aplaceforme.com',
            'password_hash': generate_password_hash('admin123'),
            'role': 'admin'
        },
        {
            'username': 'sarah_faith',
            'email': 'sarah@example.com',
            'password_hash': generate_password_hash('password123'),
            'role': 'user'
        },
        {
            'username': 'david_writer',
            'email': 'david@example.com',
            'password_hash': generate_password_hash('password123'),
            'role': 'author'
        },
        {
            'username': 'maria_singer',
            'email': 'maria@example.com',
            'password_hash': generate_password_hash('password123'),
            'role': 'user'
        },
        {
            'username': 'james_mentor',
            'email': 'james@example.com',
            'password_hash': generate_password_hash('password123'),
            'role': 'author'
        }
    ]
    
    created_users = []
    for user_data in users:
        user = User(**user_data)
        db.session.add(user)
        created_users.append(user)
    
    return created_users

def create_sample_blog_posts(users):
    """Create sample blog posts."""
    blog_posts = [
        {
            'title': 'Finding Hope in Difficult Times',
            'content': '''Life has a way of throwing curveballs when we least expect them. Whether it's loss, disappointment, or uncertainty about the future, we all face moments that test our faith and resilience.

But I've learned that hope isn't just a feeling—it's a choice. It's the decision to believe that God has a plan, even when we can't see it. It's trusting that He is working all things together for good, even in the midst of our struggles.

Today, I want to encourage you to hold onto hope. Not the kind that depends on circumstances, but the kind that is anchored in God's unchanging love for you. Remember, every storm eventually passes, and the sun will shine again.

"For I know the plans I have for you," declares the Lord, "plans to prosper you and not to harm you, plans to give you hope and a future." - Jeremiah 29:11''',
            'author_id': 1,  # admin
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=5),
        },
        {
            'title': 'The Power of Gratitude',
            'content': '''Gratitude has the power to transform our perspective and change our hearts. When we focus on what we have rather than what we lack, we begin to see God's goodness in every aspect of our lives.

I challenge you to start a gratitude journal. Each day, write down three things you're thankful for. They don't have to be big things—sometimes it's the small blessings that make the biggest difference.

Maybe it's the warmth of your morning coffee, a text from a friend, or the sound of rain on your roof. When we train our hearts to notice these gifts, we realize how abundantly blessed we truly are.

"Give thanks in all circumstances; for this is God's will for you in Christ Jesus." - 1 Thessalonians 5:18''',
            'author_id': 2,  # sarah
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=3),
        },
        {
            'title': 'Walking by Faith, Not by Sight',
            'content': '''Faith is believing in what we cannot see. It's trusting God's promises even when our circumstances suggest otherwise. This isn't always easy, but it's in these moments that our faith grows stronger.

I remember a time when I faced a major decision and had no clear direction. I prayed, sought counsel, and still felt uncertain. But I took a step of faith, trusting that God would guide me. Looking back, I can see how He was directing my path all along.

Faith isn't about having all the answers. It's about trusting the One who does. When we walk by faith, we discover that God is always faithful to provide what we need, when we need it.

"For we live by faith, not by sight." - 2 Corinthians 5:7''',
            'author_id': 3,  # david
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=1),
        },
        {
            'title': 'Building Community in Faith',
            'content': '''We were never meant to journey through life alone. God designed us for community, for relationships that encourage, support, and challenge us to grow.

In our digital age, it's easy to feel disconnected despite being more "connected" than ever. But true community goes beyond social media likes and comments. It's about being present with one another, sharing our joys and struggles, and walking together in faith.

Whether it's joining a small group, volunteering in your community, or simply reaching out to a neighbor, there are countless ways to build meaningful connections. When we invest in others, we discover that we're enriched in return.

"As iron sharpens iron, so one person sharpens another." - Proverbs 27:17''',
            'author_id': 4,  # maria
            'is_published': True,
            'publish_at': datetime.now() - timedelta(hours=6),
        },
        {
            'title': 'Finding Your Purpose',
            'content': '''Every person has a unique purpose, a special calling that only they can fulfill. Sometimes we spend so much time looking at what others are doing that we miss our own path.

Your purpose isn't necessarily your job or career, though it might be. It's about using your gifts, talents, and experiences to make a positive impact in the world. It's about being who God created you to be.

Don't compare your journey to others. God has given each of us different gifts for a reason. Your story, your struggles, and your victories are all part of preparing you for your purpose.

Trust the process. God is still writing your story, and the best chapters may be yet to come.

"For we are God's handiwork, created in Christ Jesus to do good works, which God prepared in advance for us to do." - Ephesians 2:10''',
            'author_id': 5,  # james
            'is_published': True,
            'publish_at': datetime.now() - timedelta(hours=2),
        }
    ]
    
    created_posts = []
    for post_data in blog_posts:
        post = BlogPost(**post_data)
        db.session.add(post)
        created_posts.append(post)
    
    return created_posts

def create_sample_god_stories(users):
    """Create sample God stories."""
    god_stories = [
        {
            'title': 'A Miracle in the Hospital',
            'content': '''Two years ago, my daughter was diagnosed with a rare condition that doctors said had no cure. The prognosis was devastating, and we were told to prepare for the worst.

But our church family rallied around us. They prayed, brought meals, and offered unwavering support. We prayed for a miracle, not knowing if it would come in the form of healing or strength to endure.

After months of treatment and prayer, the doctors were amazed. The condition that had no cure was completely gone. The medical team called it unexplained, but we knew exactly what had happened.

God had intervened in a way that only He could. Today, my daughter is healthy and thriving, a living testimony to the power of prayer and the faithfulness of God.

Sometimes miracles come in quiet moments, and sometimes they're dramatic. This was our dramatic moment, and we'll never forget God's goodness to our family.''',
            'author_id': 2,  # sarah
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=4),
        },
        {
            'title': 'Provision in Unexpected Ways',
            'content': '''After losing my job during a company restructure, I was worried about how I'd provide for my family. We had been living paycheck to paycheck, and the future seemed uncertain.

I prayed for wisdom and opportunity, trusting that God would provide. Within a week, I received a call from a company I had never applied to. Apparently, a friend had recommended me for a position that was a perfect fit for my skills.

Not only did I get the job, but it came with a significant salary increase and better benefits. What seemed like a setback became a setup for God's blessing.

Looking back, I realize that God was preparing this opportunity long before I lost my first job. He sees the bigger picture when we can only see the present moment.

His provision often comes in ways we never expected, but always at the perfect time.''',
            'author_id': 3,  # david
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=2),
        },
        {
            'title': 'Restored Relationship',
            'content': '''My sister and I hadn't spoken in three years following a family disagreement. The hurt ran deep, and pride kept us apart. I often thought about reaching out, but fear of rejection held me back.

One morning during my prayer time, I felt a strong urge to call her. I almost ignored it, but something inside me knew this was God's prompting. With trembling hands, I dialed her number.

She answered, and to my surprise, she had been thinking about me too. We both apologized, cried, and talked for hours. It was as if the years of silence melted away in that conversation.

Today, our relationship is stronger than ever. We learned that forgiveness isn't always easy, but it's always worth it. God restored what we thought was permanently broken.

Sometimes the greatest miracles happen in the human heart.''',
            'author_id': 4,  # maria
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=1),
        },
        {
            'title': 'Finding Peace in the Storm',
            'content': '''When my husband was deployed overseas, I felt overwhelmed by the responsibility of raising our two young children alone. The worry about his safety, combined with the daily challenges of single parenting, left me exhausted and anxious.

One particularly difficult night, after the kids had finally fallen asleep, I broke down in tears. I felt so alone and afraid. In that moment, I cried out to God for peace and strength.

Suddenly, I felt a warmth wash over me, and the most incredible sense of peace filled my heart. It was as if God was physically holding me, assuring me that everything would be okay.

From that night forward, whenever anxiety tried to creep in, I remembered that feeling of God's presence. It sustained me through the entire deployment and continues to be my anchor in difficult times.

God's peace truly does surpass all understanding.''',
            'author_id': 5,  # james
            'is_published': True,
            'publish_at': datetime.now() - timedelta(hours=8),
        },
        {
            'title': 'The Divine Appointment',
            'content': '''I was having a terrible day. Everything that could go wrong seemed to go wrong. I was running late for an important meeting when my car broke down on the highway.

While waiting for roadside assistance, I noticed an elderly man struggling with his own car troubles nearby. Despite my own stress, I felt compelled to help him. We worked together to get his car running again.

During our conversation, I learned that he was a retired businessman who had been praying for guidance about a new venture. As we talked, I realized that my skills and experience were exactly what he needed for his project.

What started as a frustrating car breakdown turned into a divine appointment. Not only did he become a business partner, but he also became a dear friend and mentor.

God can use even our worst days to orchestrate His perfect plan.''',
            'author_id': 1,  # admin
            'is_published': True,
            'publish_at': datetime.now() - timedelta(hours=4),
        }
    ]
    
    created_stories = []
    for story_data in god_stories:
        story = GodStory(**story_data)
        db.session.add(story)
        created_stories.append(story)
    
    return created_stories

def create_sample_songs(users):
    """Create sample songs."""
    songs = [
        {
            'title': 'Amazing Grace',
            'artist': 'Traditional',
            'album': 'Classic Hymns',
            'duration': 240,  # 4 minutes
            'genre': 'Hymn',
That saved a wretch like me
I once was lost, but now I'm found
Was blind, but now I see

'Twas grace that taught my heart to fear
And grace my fears relieved
How precious did that grace appear
The hour I first believed''',
            'uploaded_by': 1,  # admin
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=7),
        },
        {
            'title': 'How Great Thou Art',
            'artist': 'Traditional',
            'album': 'Worship Classics',
            'duration': 180,  # 3 minutes
            'genre': 'Hymn',
Consider all the worlds thy hands have made
I see the stars, I hear the rolling thunder
Thy power throughout the universe displayed

Then sings my soul, my Saviour God, to thee
How great thou art, how great thou art
Then sings my soul, my Saviour God, to thee
How great thou art, how great thou art''',
            'uploaded_by': 4,  # maria
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=5),
        },
        {
            'title': 'Blessed Assurance',
            'artist': 'Fanny Crosby',
            'album': 'Heart Songs',
            'duration': 200,  # 3:20
            'genre': 'Hymn',
Oh, what a foretaste of glory divine
Heir of salvation, purchase of God
Born of His Spirit, washed in His blood

This is my story, this is my song
Praising my Savior all the day long
This is my story, this is my song
Praising my Savior all the day long''',
            'uploaded_by': 2,  # sarah
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=3),
        },
        {
            'title': 'Be Thou My Vision',
            'artist': 'Irish Traditional',
            'album': 'Celtic Worship',
            'duration': 220,  # 3:40
            'genre': 'Celtic Hymn',
Naught be all else to me, save that thou art
Thou my best thought, by day or by night
Waking or sleeping, thy presence my light

Be thou my wisdom, and thou my true word
I ever with thee and thou with me, Lord
Thou my great Father, I thy true son
Thou in me dwelling, and I with thee one''',
            'uploaded_by': 3,  # david
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=1),
        },
        {
            'title': 'It Is Well With My Soul',
            'artist': 'Horatio Spafford',
            'album': 'Songs of Hope',
            'duration': 260,  # 4:20
            'genre': 'Hymn',
When sorrows like sea billows roll
Whatever my lot, thou hast taught me to say
It is well, it is well with my soul

It is well (it is well)
With my soul (with my soul)
It is well, it is well with my soul''',
            'uploaded_by': 5,  # james
            'is_published': True,
            'publish_at': datetime.now() - timedelta(hours=12),
        }
    ]
    
    created_songs = []
    for song_data in songs:
        song = Song(**song_data)
        db.session.add(song)
        created_songs.append(song)
    
    return created_songs

def create_sample_testimonials(users):
    """Create sample testimonials."""
    testimonials = [
        {
            'author_name': 'Sarah Johnson',
            'author_email': 'sarah@example.com',
            'content': '''This platform has been a beacon of hope in my life. The God stories shared here remind me daily of His faithfulness and love. During a particularly difficult season, reading about others' experiences with God's provision gave me the courage to keep trusting.

The community here is genuine and supportive. I've found prayer partners and friends who truly understand the journey of faith. Thank you for creating such a safe space for believers to connect and grow together.''',
            'author_id': 2,  # sarah
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=6),
        },
        {
            'title': 'Life-Changing Music',
            'author_name': 'David Miller',
            'author_email': 'david@example.com',
            'content': '''The music and radio sessions have transformed my morning routine. I start each day with worship and teaching that sets my heart in the right direction. The songs available here have become the soundtrack to my spiritual journey.

What I love most is how the music connects to real-life stories and experiences. It's not just entertainment—it's ministry that speaks directly to where I am in my walk with God.''',
            'author_id': 3,  # david
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=4),
        },
        {
            'title': 'Found My Voice',
            'author_name': 'Maria Rodriguez',
            'author_email': 'maria@example.com',
            'content': '''As someone who leads worship at my church, I've found incredible resources and inspiration here. The blend of traditional hymns with contemporary expression has helped me grow as both a musician and a worship leader.

But more than that, this platform has helped me find my voice in sharing my own story. Reading others' testimonials gave me the courage to be vulnerable about my own struggles and victories.''',
            'author_id': 4,  # maria
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=2),
        },
        {
            'title': 'Weekly Encouragement',
            'author_name': 'James Wilson',
            'author_email': 'james@example.com',
            'content': '''Finding this community was exactly what I needed. The newsletter keeps me connected and inspired throughout the week. Even when I'm too busy to visit the site, those weekly emails remind me of God's faithfulness and love.

The content is always relevant and practical. It's not just theoretical—it's real-life application of faith that helps me navigate challenges and celebrate victories.''',
            'author_id': 5,  # james
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=1),
        },
        {
            'title': 'Digital Sanctuary',
            'author_name': 'Lisa Chen',
            'author_email': 'lisa@example.com',
            'content': '''In our busy world, it's hard to find quiet moments with God. This platform has become my digital sanctuary—a place where I can retreat, reflect, and be refreshed.

The blog posts offer deep spiritual insight, while the testimonials remind me that I'm not alone in my struggles. The music lifts my spirit, and the community prays with me through both joys and challenges.

This truly is "a place for me" in every sense of the phrase.''',
            'author_id': 1,  # admin (representing external user)
            'is_published': True,
            'publish_at': datetime.now() - timedelta(hours=6),
        }
    ]
    
    created_testimonials = []
    for testimonial_data in testimonials:
        testimonial = Testimonial(**testimonial_data)
        db.session.add(testimonial)
        created_testimonials.append(testimonial)
    
    return created_testimonials

def create_sample_subscribers():
    """Create sample subscribers."""
    subscribers = [
        {
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_active': True,
            'subscribed_at': datetime.now() - timedelta(days=30),
            'preferences': 'weekly_newsletter,blog_updates'
        },
        {
            'email': 'jane.smith@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'is_active': True,
            'subscribed_at': datetime.now() - timedelta(days=25),
            'preferences': 'weekly_newsletter,music_updates,radio_sessions'
        },
        {
            'email': 'robert.johnson@example.com',
            'first_name': 'Robert',
            'last_name': 'Johnson',
            'is_active': True,
            'subscribed_at': datetime.now() - timedelta(days=20),
            'preferences': 'weekly_newsletter,blog_updates,testimonials'
        },
        {
            'email': 'emily.davis@example.com',
            'first_name': 'Emily',
            'last_name': 'Davis',
            'is_active': True,
            'subscribed_at': datetime.now() - timedelta(days=15),
            'preferences': 'weekly_newsletter,god_stories,music_updates'
        },
        {
            'email': 'michael.brown@example.com',
            'first_name': 'Michael',
            'last_name': 'Brown',
            'is_active': True,
            'subscribed_at': datetime.now() - timedelta(days=10),
            'preferences': 'weekly_newsletter,blog_updates,radio_sessions,testimonials'
        }
    ]
    
    created_subscribers = []
    for subscriber_data in subscribers:
        subscriber = Subscriber(**subscriber_data)
        db.session.add(subscriber)
        created_subscribers.append(subscriber)
    
    return created_subscribers

def create_sample_newsletters():
    """Create sample newsletters."""
    newsletters = [
        {
            'subject': 'Weekly Inspiration - Finding Hope in Every Season',
            'body': '''Dear Friends,

This week, I want to encourage you with a simple truth: God is present in every season of your life. Whether you're experiencing a season of joy, challenge, growth, or waiting, He is there with you.

🌟 **This Week's Highlights:**
- New blog post: "Finding Hope in Difficult Times" - A personal reflection on trusting God through uncertainty
- God Story spotlight: "A Miracle in the Hospital" - A testimony of divine healing and community support
- New music: "Amazing Grace" - A timeless hymn that reminds us of God's unending love

📖 **Scripture for the Week:**
"For I know the plans I have for you," declares the Lord, "plans to prosper you and not to harm you, plans to give you hope and a future." - Jeremiah 29:11

🙏 **Prayer Request:**
Please pray for our community member Sarah as she navigates her daughter's health journey. Pray for healing, peace, and strength for their family.

Remember, you are loved, you are chosen, and you have a purpose. Have a blessed week!

With love and prayers,
A Place For Me Community''',
            'sent_at': datetime.now() - timedelta(days=7),
            'recipients_count': 5,
            'status': 'sent'
        },
        {
            'subject': 'Weekly Inspiration - The Power of Gratitude',
            'body': '''Hello Beautiful Souls,

As we enter this new week, I want to challenge you to embrace the power of gratitude. When we shift our focus from what we lack to what we have, our entire perspective changes.

🌟 **This Week's Highlights:**
- New blog post: "The Power of Gratitude" - Practical ways to cultivate thankfulness in daily life
- God Story update: "Provision in Unexpected Ways" - How God provides even when we can't see His plan
- Music meditation: "How Great Thou Art" - A worship experience that lifts our hearts

📖 **Scripture for the Week:**
"Give thanks in all circumstances; for this is God's will for you in Christ Jesus." - 1 Thessalonians 5:18

🙏 **Community Prayer:**
We're grateful for each member of our community. Thank you for sharing your stories, your struggles, and your victories with us.

Take a moment today to write down three things you're thankful for. Watch how it transforms your heart!

Blessings and gratitude,
A Place For Me Team''',
            'sent_at': datetime.now() - timedelta(days=14),
            'recipients_count': 5,
            'status': 'sent'
        },
        {
            'subject': 'Weekly Inspiration - Walking by Faith',
            'body': '''Dear Faith Family,

Faith isn't about having all the answers—it's about trusting the One who does. This week, let's explore what it means to walk by faith, not by sight.

🌟 **This Week's Highlights:**
- New blog post: "Walking by Faith, Not by Sight" - Trusting God when you can't see the path
- God Story feature: "Restored Relationship" - How God mends what seems broken beyond repair
- Worship song: "Blessed Assurance" - A declaration of confidence in God's promises

📖 **Scripture for the Week:**
"For we live by faith, not by sight." - 2 Corinthians 5:7

🙏 **Faith Challenge:**
This week, take one step of faith. Whether it's having a difficult conversation, starting something new, or simply trusting God with your worries—step out in faith.

Remember, God's faithfulness is your foundation. He will never leave you nor forsake you.

Walking alongside you,
A Place For Me Community''',
            'sent_at': datetime.now() - timedelta(days=21),
            'recipients_count': 5,
            'status': 'sent'
        },
        {
            'subject': 'Weekly Inspiration - Building Community',
            'body': '''Beloved Community,

We were created for connection. This week, let's celebrate the beauty of community and explore ways to build deeper, more meaningful relationships.

🌟 **This Week's Highlights:**
- New blog post: "Building Community in Faith" - The importance of authentic relationships
- God Story inspiration: "The Divine Appointment" - How God orchestrates unexpected connections
- Community song: "Be Thou My Vision" - A prayer for God's guidance in all our relationships

📖 **Scripture for the Week:**
"As iron sharpens iron, so one person sharpens another." - Proverbs 27:17

🙏 **Community Action:**
Reach out to someone this week. Send an encouraging text, make a phone call, or simply be present with someone who needs it.

You are not alone in this journey. We're here, walking together in faith and love.

With community love,
A Place For Me Family''',
            'sent_at': datetime.now() - timedelta(days=28),
            'recipients_count': 5,
            'status': 'sent'
        },
        {
            'subject': 'Weekly Inspiration - Finding Your Purpose',
            'body': '''Precious Friends,

God has a unique purpose for each of us. This week, let's explore how to discover and embrace the calling He has placed on your life.

🌟 **This Week's Highlights:**
- New blog post: "Finding Your Purpose" - Discovering God's unique plan for your life
- God Story testimony: "Finding Peace in the Storm" - How God's presence sustains us through difficult times
- Worship moment: "It Is Well With My Soul" - Finding peace in God's perfect plan

📖 **Scripture for the Week:**
"For we are God's handiwork, created in Christ Jesus to do good works, which God prepared in advance for us to do." - Ephesians 2:10

🙏 **Purpose Prayer:**
Ask God to reveal His purpose for your life. Be patient, be open, and trust His timing.

Your story is still being written, and the best chapters may be yet to come!

With purposeful love,
A Place For Me Ministry''',
            'sent_at': datetime.now() - timedelta(days=35),
            'recipients_count': 5,
            'status': 'sent'
        }
    ]
    
    created_newsletters = []
    for newsletter_data in newsletters:
        newsletter = Newsletter(**newsletter_data)
        db.session.add(newsletter)
        created_newsletters.append(newsletter)
    
    return created_newsletters

def create_sample_radio_sessions():
    """Create sample radio sessions."""
    radio_sessions = [
        {
            'title': 'Morning Devotion - Finding Hope in Scripture',
            'description': 'Join us for a peaceful morning devotion as we explore biblical passages that offer hope and encouragement for daily life.',
            'duration': 1800,  # 30 minutes
            'host': 'Pastor Mike',
            'recorded_at': datetime.now() - timedelta(days=1),
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=1),
        },
        {
            'title': 'Worship Wednesday - Hymns of Faith',
            'description': 'A mid-week worship experience featuring classic hymns and contemporary arrangements that celebrate our faith.',
            'duration': 2400,  # 40 minutes
            'host': 'Maria Rodriguez',
            'recorded_at': datetime.now() - timedelta(days=3),
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=3),
        },
        {
            'title': 'Faith Stories - Community Testimonies',
            'description': 'Listen to inspiring testimonies from our community members as they share how God has worked in their lives.',
            'duration': 2700,  # 45 minutes
            'host': 'David Miller',
            'recorded_at': datetime.now() - timedelta(days=5),
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=5),
        },
        {
            'title': 'Prayer and Meditation - Finding Peace',
            'description': 'A guided prayer and meditation session to help you find peace and connect with God in the midst of life\'s busyness.',
            'duration': 1200,  # 20 minutes
            'host': 'Sarah Johnson',
            'recorded_at': datetime.now() - timedelta(days=7),
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=7),
        },
        {
            'title': 'Sunday Reflection - Walking in Purpose',
            'description': 'A Sunday evening reflection on discovering and living out God\'s purpose for your life, with practical application and encouragement.',
            'duration': 2100,  # 35 minutes
            'host': 'James Wilson',
            'recorded_at': datetime.now() - timedelta(days=2),
            'is_published': True,
            'publish_at': datetime.now() - timedelta(days=2),
        }
    ]
    
    created_sessions = []
    for session_data in radio_sessions:
        session = RadioSession(**session_data)
        db.session.add(session)
        created_sessions.append(session)
    
    return created_sessions

def create_sample_session_tokens(users):
    """Create sample session tokens for testing."""
    tokens = []
    for i, user in enumerate(users[:3]):  # Only create tokens for first 3 users
        token = SessionToken(
            user_id=user.id,
            token=f'sample_token_{i+1}_{datetime.now().strftime("%Y%m%d")}',
            expires_at=datetime.now() + timedelta(days=7)
        )
        tokens.append(token)
        db.session.add(token)
    
    return tokens

def create_sample_log_entries():
    """Create sample log entries."""
    log_entries = [
        {
            'level': 'INFO',
            'message': 'User admin logged in successfully',
            'user_id': 1,
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'level': 'INFO',
            'message': 'New blog post published: Finding Hope in Difficult Times',
            'user_id': 1,
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': datetime.now() - timedelta(days=5)
        },
        {
            'level': 'INFO',
            'message': 'New subscriber registered: john.doe@example.com',
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'created_at': datetime.now() - timedelta(days=30)
        },
        {
            'level': 'INFO',
            'message': 'Newsletter sent: Weekly Inspiration - Finding Hope in Every Season',
            'user_id': 1,
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': datetime.now() - timedelta(days=7)
        },
        {
            'level': 'INFO',
            'message': 'New radio session published: Morning Devotion - Finding Hope in Scripture',
            'user_id': 1,
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': datetime.now() - timedelta(days=1)
        }
    ]
    
    created_logs = []
    for log_data in log_entries:
        log = LogEntry(**log_data)
        db.session.add(log)
        created_logs.append(log)
    
    return created_logs

def seed_database():
    """Main function to seed the database with sample data."""
    print("🌱 Starting database seeding...")
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("🗑️  Clearing existing data...")
        db.session.query(LogEntry).delete()
        db.session.query(SessionToken).delete()
        db.session.query(RadioSession).delete()
        db.session.query(Newsletter).delete()
        db.session.query(Subscriber).delete()
        db.session.query(Testimonial).delete()
        db.session.query(Song).delete()
        db.session.query(GodStory).delete()
        db.session.query(BlogPost).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create sample data
        print("👥 Creating sample users...")
        users = create_sample_users()
        db.session.commit()
        
        print("📝 Creating sample blog posts...")
        blog_posts = create_sample_blog_posts(users)
        db.session.commit()
        
        print("✨ Creating sample God stories...")
        god_stories = create_sample_god_stories(users)
        db.session.commit()
        
        print("🎵 Creating sample songs...")
        songs = create_sample_songs(users)
        db.session.commit()
        
        print("💬 Creating sample testimonials...")
        testimonials = create_sample_testimonials(users)
        db.session.commit()
        
        print("📧 Creating sample subscribers...")
        subscribers = create_sample_subscribers()
        db.session.commit()
        
        print("📰 Creating sample newsletters...")
        newsletters = create_sample_newsletters()
        db.session.commit()
        
        print("📻 Creating sample radio sessions...")
        radio_sessions = create_sample_radio_sessions()
        db.session.commit()
        
        print("🔑 Creating sample session tokens...")
        session_tokens = create_sample_session_tokens(users)
        db.session.commit()
        
        print("📊 Creating sample log entries...")
        log_entries = create_sample_log_entries()
        db.session.commit()
        
        print("✅ Database seeding completed successfully!")
        print(f"   - Created {len(users)} users")
        print(f"   - Created {len(blog_posts)} blog posts")
        print(f"   - Created {len(god_stories)} God stories")
        print(f"   - Created {len(songs)} songs")
        print(f"   - Created {len(testimonials)} testimonials")
        print(f"   - Created {len(subscribers)} subscribers")
        print(f"   - Created {len(newsletters)} newsletters")
        print(f"   - Created {len(radio_sessions)} radio sessions")
        print(f"   - Created {len(session_tokens)} session tokens")
        print(f"   - Created {len(log_entries)} log entries")
        
        print("\n🔐 Admin Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        
        print("\n👤 Sample User Credentials:")
        print("   Username: sarah_faith | Password: password123")
        print("   Username: david_writer | Password: password123")
        print("   Username: maria_singer | Password: password123")
        print("   Username: james_mentor | Password: password123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    # Create Flask app and initialize database
    config_vars = {k: getattr(config, k) for k in dir(config) if not k.startswith("__")}
    app = create_app(config_vars)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed the database
        seed_database()
