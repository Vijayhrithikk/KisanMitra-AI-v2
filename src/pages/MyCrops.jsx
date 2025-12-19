import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
    Leaf, Plus, AlertTriangle, Calendar, MapPin, Droplets,
    ChevronRight, RefreshCw, Loader2, Bell, Search, TrendingUp, Trash2
} from 'lucide-react';
import './MyCrops.css';

const API_BASE = import.meta.env.VITE_ML_API_URL || 'http://localhost:8001';

const MyCrops = () => {
    const { i18n } = useTranslation();
    const navigate = useNavigate();
    const lang = i18n.language === 'te' ? 'te' : 'en';

    const [loading, setLoading] = useState(true);
    const [subscriptions, setSubscriptions] = useState([]);
    const [error, setError] = useState(null);
    const [deleting, setDeleting] = useState(null); // Track which subscription is being deleted

    // Get farmer ID from localStorage
    const farmerId = localStorage.getItem('farmerPhone') || '7330671778';

    // Crop icons mapping
    const cropIcons = {
        'Paddy': '🌾', 'Rice': '🌾', 'Cotton': '🧶', 'Maize': '🌽',
        'Chilli': '🌶️', 'Groundnut': '🥜', 'Ground Nuts': '🥜',
        'Wheat': '🌾', 'Sugarcane': '🎋', 'Tomato': '🍅',
        'Pulses': '🫘', 'Turmeric': '🟡', 'Banana': '🍌'
    };

    // Labels
    const L = {
        title: lang === 'te' ? '🌾 నా పంటలు' : '🌾 My Crops',
        subtitle: lang === 'te' ? 'మీ పంటల రోజువారీ మానిటరింగ్' : 'Daily monitoring for your crops',
        addCrop: lang === 'te' ? '+ కొత్త పంట జోడించండి' : '+ Add New Crop',
        noCrops: lang === 'te' ? 'ఇంకా పంటలు జోడించలేదు' : 'No crops added yet',
        addFirst: lang === 'te' ? 'మీ మొదటి పంటను జోడించండి' : 'Add your first crop to start monitoring',
        day: lang === 'te' ? 'రోజు' : 'Day',
        stage: lang === 'te' ? 'దశ' : 'Stage',
        alerts: lang === 'te' ? 'హెచ్చరికలు' : 'Alerts',
        viewPlan: lang === 'te' ? 'రోజు ప్లాన్ చూడండి' : 'View Daily Plan',
        refresh: lang === 'te' ? 'రిఫ్రెష్' : 'Refresh',
        area: lang === 'te' ? 'విస్తీర్ణం' : 'Area',
        acres: lang === 'te' ? 'ఎకరాలు' : 'acres',
        delete: lang === 'te' ? 'తొలగించు' : 'Delete',
        confirmDelete: lang === 'te' ? 'నిజంగా తొలగించాలా?' : 'Really delete?',
        yes: lang === 'te' ? 'అవును' : 'Yes',
        no: lang === 'te' ? 'కాదు' : 'No'
    };

    useEffect(() => {
        fetchSubscriptions();
    }, []);

    const fetchSubscriptions = async () => {
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE}/my-crops/${farmerId}`);
            const data = await res.json();
            if (data.success) {
                setSubscriptions(data.subscriptions);
            } else {
                setError('Failed to load crops');
            }
        } catch (err) {
            console.error(err);
            setError('Connection error');
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (e, subscriptionId) => {
        e.stopPropagation(); // Prevent card click
        if (deleting === subscriptionId) {
            // Already confirming - do the delete
            try {
                const res = await fetch(`${API_BASE}/subscription/${subscriptionId}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    setSubscriptions(prev => prev.filter(s => s.subscriptionId !== subscriptionId));
                }
            } catch (err) {
                console.error('Delete failed:', err);
            }
            setDeleting(null);
        } else {
            // First click - show confirmation
            setDeleting(subscriptionId);
            setTimeout(() => setDeleting(null), 3000); // Auto-cancel after 3s
        }
    };

    const getProgressColor = (percent) => {
        if (percent < 30) return '#22c55e';
        if (percent < 60) return '#eab308';
        if (percent < 85) return '#f97316';
        return '#ef4444';
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return date.toLocaleDateString(lang === 'te' ? 'te-IN' : 'en-IN', {
            day: 'numeric', month: 'short'
        });
    };

    if (loading) {
        return (
            <div className="mycrops-container">
                <div className="loading-state">
                    <Loader2 className="spinner" size={40} />
                    <p>{lang === 'te' ? 'లోడ్ అవుతోంది...' : 'Loading your crops...'}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="mycrops-container">
            {/* Header */}
            <div className="mycrops-header">
                <div className="header-content">
                    <h1>{L.title}</h1>
                    <p>{L.subtitle}</p>
                </div>
                <button className="refresh-btn" onClick={fetchSubscriptions}>
                    <RefreshCw size={18} />
                </button>
            </div>

            {/* Add New Crop Button */}
            <button
                className="add-crop-btn"
                onClick={() => navigate('/subscribe-crop')}
            >
                <Plus size={20} />
                {L.addCrop}
            </button>

            {/* Crops List */}
            {subscriptions.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-icon">🌱</div>
                    <h3>{L.noCrops}</h3>
                    <p>{L.addFirst}</p>
                    <button
                        className="start-btn"
                        onClick={() => navigate('/subscribe-crop')}
                    >
                        <Plus size={20} />
                        {L.addCrop}
                    </button>
                </div>
            ) : (
                <div className="crops-list">
                    {subscriptions.map((sub) => {
                        const stageInfo = sub.stage_info || {};
                        const progress = stageInfo.progress_percent || 0;
                        const hasAlerts = sub.has_urgent_alerts;
                        const alertCount = sub.alert_count || 0;

                        return (
                            <div
                                key={sub.subscriptionId}
                                className={`crop-card ${hasAlerts ? 'has-alerts' : ''}`}
                                onClick={() => navigate(`/monitor/${sub.subscriptionId}`)}
                            >
                                {/* Alert Badge */}
                                {alertCount > 0 && (
                                    <div className="alert-badge">
                                        <Bell size={14} />
                                        {alertCount}
                                    </div>
                                )}

                                {/* Crop Header */}
                                <div className="crop-header">
                                    <div className="crop-icon">
                                        {cropIcons[sub.crop] || '🌱'}
                                    </div>
                                    <div className="crop-info">
                                        <h3>{sub.crop}</h3>
                                        <div className="crop-meta">
                                            <span><MapPin size={14} /> {sub.location?.name || sub.locationName}</span>
                                            <span><Droplets size={14} /> {sub.areaAcres} {L.acres}</span>
                                        </div>
                                    </div>
                                    <ChevronRight size={24} className="chevron" />
                                </div>

                                {/* Progress Bar */}
                                <div className="progress-section">
                                    <div className="progress-header">
                                        <span className="stage-name">
                                            {stageInfo.stage_name || 'Growing'}
                                        </span>
                                        <span className="day-count">
                                            {L.day} {stageInfo.days_after_sowing || 0}
                                        </span>
                                    </div>
                                    <div className="progress-bar">
                                        <div
                                            className="progress-fill"
                                            style={{
                                                width: `${progress}%`,
                                                backgroundColor: getProgressColor(progress)
                                            }}
                                        />
                                    </div>
                                    <div className="progress-labels">
                                        <span>{formatDate(sub.sowingDate)}</span>
                                        <span>{progress}%</span>
                                        <span>{formatDate(stageInfo.harvest_expected)}</span>
                                    </div>
                                </div>

                                {/* Quick Stats */}
                                <div className="quick-stats">
                                    {hasAlerts ? (
                                        <div className="stat alert">
                                            <AlertTriangle size={16} />
                                            <span>{alertCount} {L.alerts}</span>
                                        </div>
                                    ) : (
                                        <div className="stat success">
                                            <TrendingUp size={16} />
                                            <span>{lang === 'te' ? 'మంచి పరిస్థితి' : 'Good condition'}</span>
                                        </div>
                                    )}
                                    <button className="view-plan-btn">
                                        {L.viewPlan}
                                        <ChevronRight size={16} />
                                    </button>
                                    <button
                                        className={`delete-btn ${deleting === sub.subscriptionId ? 'confirming' : ''}`}
                                        onClick={(e) => handleDelete(e, sub.subscriptionId)}
                                    >
                                        <Trash2 size={16} />
                                        {deleting === sub.subscriptionId ? L.yes : ''}
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {/* Quick Actions */}
            <div className="quick-actions">
                <button onClick={() => navigate('/recommend')}>
                    <Search size={20} />
                    <span>{lang === 'te' ? 'పంట సిఫార్సు' : 'Crop Recommendation'}</span>
                </button>
                <button onClick={() => navigate('/advisory')}>
                    <Calendar size={20} />
                    <span>{lang === 'te' ? 'పంట సలహా' : 'Crop Advisory'}</span>
                </button>
            </div>
        </div>
    );
};

export default MyCrops;
