import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import LanguageSelector from '../components/LanguageSelector';
import ModernTechniquesCarousel from '../components/ModernTechniquesCarousel';
import { marketService } from '../services/marketService';
import {
    Leaf, Store, Tractor, CloudSun, MapPin, Search,
    ChevronRight, Package, Plus, User, Settings, Droplets
} from 'lucide-react';
import './Home.css';

const Home = () => {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();
    const { user, isLoggedIn } = useAuth() || {};
    const lang = i18n.language === 'te' ? 'te' : 'en';

    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);

    // Localized strings
    const L = {
        greeting: lang === 'te' ? 'నమస్కారం' : 'Namaste',
        welcome: lang === 'te' ? 'కిసాన్ మిత్ర లో స్వాగతం' : 'Welcome to KisanMitra',
        subtitle: lang === 'te' ? 'మీ వ్యవసాయ సహాయకుడు' : 'Your Farming Companion',
        cropAdvisory: lang === 'te' ? 'పంట సలహా' : 'Crop Advisory',
        cropAdvisoryDesc: lang === 'te' ? 'AI ఆధారిత పంట సిఫారసులు' : 'AI-powered crop recommendations',
        marketplace: lang === 'te' ? 'మార్కెట్‌ప్లేస్' : 'Marketplace',
        marketplaceDesc: lang === 'te' ? 'మీ పంటలను అమ్మండి' : 'Sell your produce',
        rentals: lang === 'te' ? 'ట్రాక్టర్ అద్దె' : 'Equipment Rental',
        rentalsDesc: lang === 'te' ? 'వ్యవసాయ పరికరాలు అద్దెకు' : 'Rent farming equipment',
        techniques: lang === 'te' ? 'ఆధునిక పద్ధతులు' : 'Modern Techniques',
        weatherUpdate: lang === 'te' ? 'వాతావరణం' : 'Weather',
        recentListings: lang === 'te' ? 'తాజా లిస్టింగ్‌లు' : 'Recent Listings',
        viewAll: lang === 'te' ? 'అన్నీ చూడండి' : 'View All',
        createListing: lang === 'te' ? 'కొత్త లిస్టింగ్' : 'New Listing',
        myDashboard: lang === 'te' ? 'నా డాష్‌బోర్డ్' : 'My Dashboard',
        login: lang === 'te' ? 'లాగిన్' : 'Login',
        search: lang === 'te' ? 'శోధించండి...' : 'Search...',
        perQuintal: lang === 'te' ? 'క్వింటాల్' : 'Quintal',
        myCrops: lang === 'te' ? 'నా పంటలు' : 'My Crops',
        myCropsDesc: lang === 'te' ? 'రోజువారీ మానిటరింగ్ & ప్లాన్' : 'Daily monitoring & plan',
        irrigation: lang === 'te' ? 'స్మార్ట్ నీటిపారుదల' : 'Smart Irrigation',
        irrigationDesc: lang === 'te' ? 'IoT ఆధారిత ఆటోమేషన్' : 'IoT-based automation'
    };

    useEffect(() => {
        loadListings();
    }, []);

    const loadListings = async () => {
        try {
            const data = await marketService.getListings();
            setListings(data.slice(0, 4));
        } catch (error) {
            console.error('Error loading listings:', error);
        } finally {
            setLoading(false);
        }
    };

    const getLocationString = (loc) => {
        if (!loc) return 'India';
        if (typeof loc === 'string') return loc;
        if (typeof loc === 'object') return loc.district || loc.city || 'India';
        return 'India';
    };

    return (
        <div className="home-page">
            {/* Header */}
            <header className="app-header">
                <div className="header-left">
                    <span className="app-logo">🌾</span>
                    <div className="app-title">
                        <span className="title-main">KisanMitra</span>
                        <span className="title-sub">{L.subtitle}</span>
                    </div>
                </div>
                <div className="header-right">
                    <LanguageSelector />
                    {isLoggedIn ? (
                        <button className="profile-btn" onClick={() => navigate('/profile')}>
                            <User size={20} />
                        </button>
                    ) : (
                        <button className="login-btn-small" onClick={() => navigate('/login')}>
                            {L.login}
                        </button>
                    )}
                </div>
            </header>

            {/* Welcome Section */}
            <section className="welcome-section">
                <div className="welcome-content">
                    <h1>{L.greeting}, {user?.name || (lang === 'te' ? 'రైతు' : 'Farmer')}! 👋</h1>
                    <p>{L.welcome}</p>
                </div>
                <div className="search-bar">
                    <Search size={18} className="search-icon" />
                    <input type="text" placeholder={L.search} />
                </div>
            </section>

            {/* Quick Actions */}
            <section className="quick-actions">
                <div className="action-card primary" onClick={() => navigate('/my-crops')}>
                    <div className="action-icon" style={{ background: '#DCFCE7' }}>
                        <span style={{ fontSize: '24px' }}>🌾</span>
                    </div>
                    <div className="action-content">
                        <h3>{L.myCrops}</h3>
                        <p>{L.myCropsDesc}</p>
                    </div>
                    <ChevronRight size={20} className="action-arrow" />
                </div>

                <div className="action-card" onClick={() => navigate('/recommend')}>
                    <div className="action-icon" style={{ background: '#E8F5E9' }}>
                        <Leaf size={24} color="#4CAF50" />
                    </div>
                    <div className="action-content">
                        <h3>{L.cropAdvisory}</h3>
                        <p>{L.cropAdvisoryDesc}</p>
                    </div>
                    <ChevronRight size={20} className="action-arrow" />
                </div>

                <div className="action-card" onClick={() => navigate('/market')}>
                    <div className="action-icon" style={{ background: '#FFF3E0' }}>
                        <Store size={24} color="#FF9800" />
                    </div>
                    <div className="action-content">
                        <h3>{L.marketplace}</h3>
                        <p>{L.marketplaceDesc}</p>
                    </div>
                    <ChevronRight size={20} className="action-arrow" />
                </div>

                <div className="action-card" onClick={() => navigate('/rentals')}>
                    <div className="action-icon" style={{ background: '#E3F2FD' }}>
                        <Tractor size={24} color="#2196F3" />
                    </div>
                    <div className="action-content">
                        <h3>{L.rentals}</h3>
                        <p>{L.rentalsDesc}</p>
                    </div>
                    <ChevronRight size={20} className="action-arrow" />
                </div>

                <div className="action-card" onClick={() => navigate('/irrigation')}>
                    <div className="action-icon" style={{ background: '#E0F7FA' }}>
                        <Droplets size={24} color="#00BCD4" />
                    </div>
                    <div className="action-content">
                        <h3>{L.irrigation}</h3>
                        <p>{L.irrigationDesc}</p>
                    </div>
                    <ChevronRight size={20} className="action-arrow" />
                </div>
            </section>

            {/* Techniques Carousel */}
            <ModernTechniquesCarousel />

            {/* Dashboard Access */}
            {isLoggedIn && (
                <section className="dashboard-access">
                    <button className="dashboard-btn" onClick={() => navigate('/farmer/dashboard')}>
                        <Package size={20} />
                        {L.myDashboard}
                        <ChevronRight size={18} />
                    </button>
                </section>
            )}

            {/* Bottom Navigation */}
            <nav className="bottom-nav">
                <button className="nav-item active" onClick={() => navigate('/')}>
                    <span className="nav-icon">🏠</span>
                    <span>{lang === 'te' ? 'హోమ్' : 'Home'}</span>
                </button>
                <button className="nav-item" onClick={() => navigate('/market')}>
                    <span className="nav-icon">🛒</span>
                    <span>{lang === 'te' ? 'మార్కెట్' : 'Market'}</span>
                </button>
                <button className="nav-item" onClick={() => navigate('/recommend')}>
                    <span className="nav-icon">🌱</span>
                    <span>{lang === 'te' ? 'సలహా' : 'Advisory'}</span>
                </button>
                <button className="nav-item" onClick={() => navigate('/techniques')}>
                    <span className="nav-icon">📚</span>
                    <span>{lang === 'te' ? 'పద్ధతులు' : 'Techniques'}</span>
                </button>
                <button className="nav-item" onClick={() => navigate(isLoggedIn ? '/profile' : '/login')}>
                    <span className="nav-icon">👤</span>
                    <span>{lang === 'te' ? 'ప్రొఫైల్' : 'Profile'}</span>
                </button>
            </nav>
        </div>
    );
};

export default Home;
