/**
 * Admin Dashboard for KisanMitra
 * View all listings, users, and chain stats
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { marketService } from '../services/marketService';
import { authService } from '../services/authService';
import {
    ShieldCheck, Users, Package, Link as LinkIcon,
    LogOut, CheckCircle, Clock, AlertTriangle
} from 'lucide-react';
import './Login.css';

const AdminDashboard = () => {
    const navigate = useNavigate();
    const { user, logout, isAdmin } = useAuth();

    const [listings, setListings] = useState([]);
    const [farmers, setFarmers] = useState([]);
    const [chainStats, setChainStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!isAdmin) {
            navigate('/login');
            return;
        }

        const loadData = async () => {
            setLoading(true);
            setError(null);

            try {
                // Load listings (async)
                const listingsData = await marketService.getListings();
                setListings(listingsData || []);

                // Load farmers
                const farmersResult = authService.getAllFarmers();
                if (farmersResult.success) {
                    setFarmers(farmersResult.farmers);
                }

                // Load chain stats
                try {
                    const stats = await marketService.getStats();
                    setChainStats(stats);
                } catch (e) {
                    console.log('Chain stats not available');
                }
            } catch (err) {
                console.error('Error loading admin data:', err);
                setError('Failed to load dashboard data');
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [isAdmin, navigate]);

    const handleVerifyFarmer = (farmerId) => {
        const result = authService.verifyFarmer(farmerId);
        if (result.success) {
            setFarmers(prev => prev.map(f =>
                f.id === farmerId ? { ...f, verified: true } : f
            ));
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (!isAdmin) return null;

    return (
        <div className="admin-page">
            <header className="admin-header">
                <h1>
                    <ShieldCheck size={24} />
                    Admin Dashboard
                </h1>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <span style={{ fontSize: '0.9rem', opacity: 0.8 }}>
                        {user?.email}
                    </span>
                    <button onClick={handleLogout} className="logout-btn" style={{ padding: '0.5rem 1rem' }}>
                        <LogOut size={16} /> Logout
                    </button>
                </div>
            </header>

            <div className="admin-content">
                {/* Loading State */}
                {loading && (
                    <div style={{ padding: '3rem', textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>⏳</div>
                        <div>Loading dashboard data...</div>
                    </div>
                )}

                {/* Error State */}
                {error && (
                    <div style={{ padding: '2rem', textAlign: 'center', color: '#dc2626', background: '#fef2f2', borderRadius: '8px', margin: '1rem' }}>
                        <AlertTriangle size={24} style={{ marginBottom: '0.5rem' }} />
                        <div>{error}</div>
                    </div>
                )}

                {/* Stats */}
                <div className="admin-stats">
                    <div className="stat-card">
                        <h4>Total Listings</h4>
                        <div className="value">{listings.length}</div>
                    </div>
                    <div className="stat-card">
                        <h4>Registered Farmers</h4>
                        <div className="value">{farmers.length}</div>
                    </div>
                    <div className="stat-card">
                        <h4>Verified Farmers</h4>
                        <div className="value">{farmers.filter(f => f.verified).length}</div>
                    </div>
                    <div className="stat-card">
                        <h4>Chain Status</h4>
                        <div className={`value ${chainStats?.chainValid ? 'valid' : 'invalid'}`}>
                            {chainStats?.chainValid ? '✓ Valid' : '✗ Invalid'}
                        </div>
                    </div>
                </div>

                {/* Chain Stats */}
                {chainStats && (
                    <div className="admin-section">
                        <div className="admin-section-header">
                            <h3><LinkIcon size={18} /> Blockchain Stats</h3>
                        </div>
                        <div style={{ padding: '1rem' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
                                <div>
                                    <strong>Total Blocks:</strong> {chainStats.totalBlocks}
                                </div>
                                <div>
                                    <strong>Chain Valid:</strong> {chainStats.chainValid ? 'Yes ✓' : 'No ✗'}
                                </div>
                                <div>
                                    <strong>Last Block Hash:</strong>
                                    <br />
                                    <code style={{ fontSize: '0.7rem' }}>{chainStats.lastBlockHash?.substring(0, 20)}...</code>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Farmers Table */}
                <div className="admin-section">
                    <div className="admin-section-header">
                        <h3><Users size={18} /> Registered Farmers</h3>
                    </div>
                    {farmers.length === 0 ? (
                        <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>
                            No farmers registered yet
                        </div>
                    ) : (
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Phone</th>
                                    <th>Location</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {farmers.map(farmer => (
                                    <tr key={farmer.id}>
                                        <td><code>{farmer.id}</code></td>
                                        <td>{farmer.name || '-'}</td>
                                        <td>{farmer.phone}</td>
                                        <td>{farmer.village ? `${farmer.village}, ${farmer.district}` : '-'}</td>
                                        <td>
                                            {farmer.verified ? (
                                                <span style={{ color: '#16a34a', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                                    <CheckCircle size={14} /> Verified
                                                </span>
                                            ) : farmer.verificationDoc ? (
                                                <span style={{ color: '#f59e0b', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                                    <Clock size={14} /> Pending
                                                </span>
                                            ) : (
                                                <span style={{ color: '#6b7280' }}>Unverified</span>
                                            )}
                                        </td>
                                        <td>
                                            <button
                                                className="verify-btn"
                                                onClick={() => handleVerifyFarmer(farmer.id)}
                                                disabled={farmer.verified}
                                            >
                                                {farmer.verified ? 'Verified' : 'Verify'}
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>

                {/* Listings Table */}
                <div className="admin-section">
                    <div className="admin-section-header">
                        <h3><Package size={18} /> All Listings</h3>
                    </div>
                    {listings.length === 0 ? (
                        <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>
                            No listings yet
                        </div>
                    ) : (
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Crop</th>
                                    <th>Farmer</th>
                                    <th>Price</th>
                                    <th>Status</th>
                                    <th>Hash</th>
                                </tr>
                            </thead>
                            <tbody>
                                {listings.map(listing => (
                                    <tr key={listing.listingId}>
                                        <td><code>{listing.listingId}</code></td>
                                        <td>{listing.crop} - {listing.variety}</td>
                                        <td>{listing.farmerId}</td>
                                        <td>₹{listing.price}/{listing.unit}</td>
                                        <td>
                                            <span className={`status-badge ${listing.status.toLowerCase()}`}>
                                                {listing.status}
                                            </span>
                                        </td>
                                        <td>
                                            <code style={{ fontSize: '0.7rem' }}>
                                                {listing.metaHash?.substring(0, 12)}...
                                            </code>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
