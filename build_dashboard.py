#!/usr/bin/env python3
"""
Smart Facts Dashboard Builder
Extracts Smart Facts data from the codebase and generates the dashboard HTML
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

def extract_smart_facts_from_codebase():
    """Extract Smart Facts data from the codebase files"""
    
    # Try multiple possible paths for the codebase
    possible_paths = [
        os.environ.get('CODEBASE_PATH'),
        '../hometap',  # If dashboard is in subdirectory
        '../../hometap',  # If dashboard is in subdirectory of subdirectory
        '/tmp/codebase'  # Fallback
    ]
    
    codebase_path = None
    for path in possible_paths:
        if path and os.path.exists(path):
            codebase_path = path
            break
    
    insights = []
    
    try:
        # Try to read from actual codebase files
        if codebase_path:
            insights = extract_from_files(codebase_path)
        else:
            # Fallback to hardcoded data
            insights = get_hardcoded_insights()
    except Exception as e:
        print(f"Error extracting from codebase: {e}")
        # Fallback to hardcoded data
        insights = get_hardcoded_insights()
    
    return insights

def extract_from_files(codebase_path):
    """Extract Smart Facts from actual codebase files"""
    insights = []
    
    # Read definitions file
    definitions_file = os.path.join(codebase_path, 'eng_portals/portals/portals/apps/smart_facts/definitions.py')
    templates_file = os.path.join(codebase_path, 'eng_portals/portals/portals/apps/smart_facts/display_templates.py')
    
    if os.path.exists(definitions_file) and os.path.exists(templates_file):
        # Parse the Python files to extract Smart Facts
        # This is a simplified version - you'd want more robust parsing
        with open(definitions_file, 'r') as f:
            definitions_content = f.read()
        
        with open(templates_file, 'r') as f:
            templates_content = f.read()
        
        # Extract Smart Fact definitions
        # Look for patterns like SmartFactDefinition(...)
        # This is where you'd implement the actual parsing logic
        
        # For now, return hardcoded data
        insights = get_hardcoded_insights()
    
    return insights

def get_hardcoded_insights():
    """Fallback hardcoded insights data"""
    return [
        # Static Content Insights
        {
            "id": "SMRT1",
            "content": "Interest rates can be unpredictable. But there are ways to access your equity without losing your current low mortgage rate.",
            "status": "live",
            "priority": 1,
            "isDynamic": False,
            "hasCta": True,
            "cta": {
                "text": "See ways to access equity",
                "url": "https://www.hometap.com/blog/cash-out-refinance-vs-a-home-equity-loan/"
            },
            "requiredContext": ["SYSTEM"],
            "requiresPrimaryUser": False,
            "requiresProfileComplete": False,
            "templateKeys": []
        },
        # Add more insights here...
        # This would be populated with all your Smart Facts data
    ]

def generate_dashboard_html(insights):
    """Generate the complete dashboard HTML"""
    
    # Read the base HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Facts Dashboard - Marketing Team</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .status-badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
        }
        .status-live { background-color: #dcfce7; color: #166534; }
        .status-review { background-color: #fef3c7; color: #92400e; }
        .status-draft { background-color: #e5e7eb; color: #374151; }
        .status-retired { background-color: #f3f4f6; color: #6b7280; }
        .status-archived { background-color: #fee2e2; color: #991b1b; }
    </style>
</head>
<body class="bg-gray-50">
    <div x-data="smartFactsDashboard()" class="min-h-screen">
        <!-- Header -->
        <header class="gradient-bg text-white shadow-lg">
            <div class="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12 py-6">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-3xl font-bold">Smart Facts Dashboard</h1>
                        <p class="text-blue-100 mt-1">Marketing Team - Content Management System</p>
                        <p class="text-blue-200 text-sm mt-1">Last updated: {last_updated}</p>
                    </div>
                    <div class="text-right">
                        <div class="text-2xl font-bold" x-text="stats.total"></div>
                        <div class="text-blue-100">Total Insights</div>
                    </div>
                </div>
            </div>
        </header>

        <!-- Controls -->
        <div class="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12 py-6">
            <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
                <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                    <!-- Search -->
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Search Insights</label>
                        <input 
                            type="text" 
                            x-model="searchQuery"
                            placeholder="Search by ID, content, or keywords..."
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                    </div>
                    
                    <!-- Status Filter -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                        <select 
                            x-model="statusFilter"
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">All Statuses</option>
                            <option value="live">Live</option>
                            <option value="review">Under Review</option>
                            <option value="draft">Draft</option>
                            <option value="retired">Retired</option>
                            <option value="archived">Archived</option>
                        </select>
                    </div>
                    
                    <!-- Type Filter -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Type</label>
                        <select 
                            x-model="typeFilter"
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">All Types</option>
                            <option value="static">Static Content</option>
                            <option value="dynamic">Dynamic Content</option>
                        </select>
                    </div>
                    
                    <!-- View Toggle -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">View</label>
                        <div class="flex rounded-md shadow-sm">
                            <button 
                                @click="viewMode = 'grid'"
                                :class="viewMode === 'grid' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'"
                                class="px-3 py-2 text-sm font-medium border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
                                </svg>
                            </button>
                            <button 
                                @click="viewMode = 'list'"
                                :class="viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'"
                                class="px-3 py-2 text-sm font-medium border border-gray-300 rounded-r-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Export Button -->
                <div class="mt-4 flex justify-end">
                    <button 
                        @click="exportToCSV()"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                    >
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        Export CSV
                    </button>
                </div>
            </div>

            <!-- Stats Cards -->
            <div class="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
                <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-6">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <div class="flex items-center">
                            <div class="p-2 bg-green-100 rounded-lg">
                                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div class="ml-4">
                                <p class="text-sm font-medium text-gray-600">Live</p>
                                <p class="text-2xl font-semibold text-gray-900" x-text="stats.live"></p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <div class="flex items-center">
                            <div class="p-2 bg-yellow-100 rounded-lg">
                                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div class="ml-4">
                                <p class="text-sm font-medium text-gray-600">Under Review</p>
                                <p class="text-2xl font-semibold text-gray-900" x-text="stats.review"></p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <div class="flex items-center">
                            <div class="p-2 bg-blue-100 rounded-lg">
                                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                            </div>
                            <div class="ml-4">
                                <p class="text-sm font-medium text-gray-600">Dynamic</p>
                                <p class="text-2xl font-semibold text-gray-900" x-text="stats.dynamic"></p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <div class="flex items-center">
                            <div class="p-2 bg-purple-100 rounded-lg">
                                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-10 0a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2M9 10h6M9 14h6"></path>
                                </svg>
                            </div>
                            <div class="ml-4">
                                <p class="text-sm font-medium text-gray-600">With CTA</p>
                                <p class="text-2xl font-semibold text-gray-900" x-text="stats.withCta"></p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <div class="flex items-center">
                            <div class="p-2 bg-gray-100 rounded-lg">
                                <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </div>
                            <div class="ml-4">
                                <p class="text-sm font-medium text-gray-600">Retired</p>
                                <p class="text-2xl font-semibold text-gray-900" x-text="stats.retired"></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Insights Display -->
            <div class="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
            <!-- Grid View -->
            <div x-show="viewMode === 'grid'" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                <template x-for="insight in filteredInsights" :key="insight.id">
                    <div class="bg-white rounded-lg shadow-sm p-6 card-hover">
                        <!-- Header -->
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900" x-text="insight.id"></h3>
                                <div class="flex items-center space-x-2 mt-1">
                                    <span class="status-badge" :class="'status-' + insight.status" x-text="insight.status"></span>
                                    <span x-show="insight.isDynamic" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Dynamic</span>
                                    <span x-show="insight.hasCta" class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">CTA</span>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-sm text-gray-500">Priority</div>
                                <div class="text-lg font-semibold" x-text="insight.priority"></div>
                            </div>
                        </div>

                        <!-- Content -->
                        <div class="mb-4">
                            <h4 class="text-sm font-medium text-gray-700 mb-2">Content:</h4>
                            <p class="text-gray-600 text-sm leading-relaxed" x-text="insight.content"></p>
                        </div>

                        <!-- Dynamic Variables -->
                        <div x-show="insight.templateKeys && insight.templateKeys.length > 0" class="mb-4">
                            <h4 class="text-sm font-medium text-gray-700 mb-2">Dynamic Variables:</h4>
                            <div class="flex flex-wrap gap-1">
                                <template x-for="key in insight.templateKeys" :key="key">
                                    <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded" x-text="key"></span>
                                </template>
                            </div>
                        </div>

                        <!-- CTA -->
                        <div x-show="insight.cta" class="mb-4">
                            <h4 class="text-sm font-medium text-gray-700 mb-2">Call to Action:</h4>
                            <div class="bg-gray-50 p-3 rounded">
                                <div class="text-sm font-medium text-gray-900" x-text="insight.cta.text"></div>
                                <div class="text-xs text-blue-600 mt-1 break-all" x-text="insight.cta.url"></div>
                            </div>
                        </div>

                        <!-- Requirements -->
                        <div class="text-xs text-gray-500 space-y-1">
                            <div x-show="insight.requiresPrimaryUser">✓ Requires Primary User</div>
                            <div x-show="insight.requiresProfileComplete">✓ Requires Profile Complete</div>
                            <div x-show="insight.requiredContext && insight.requiredContext.length > 0">
                                Context: <span x-text="insight.requiredContext.join(', ')"></span>
                            </div>
                        </div>
                    </div>
                </template>
            </div>

            <!-- List View -->
            <div x-show="viewMode === 'list'" class="space-y-4">
                <template x-for="insight in filteredInsights" :key="insight.id">
                    <div class="bg-white rounded-lg shadow-sm p-6 card-hover">
                        <div class="flex items-start space-x-4">
                            <!-- Left Column: ID and Status -->
                            <div class="flex-shrink-0 w-32">
                                <h3 class="text-lg font-semibold text-gray-900" x-text="insight.id"></h3>
                                <div class="flex flex-col space-y-2 mt-2">
                                    <span class="status-badge" :class="'status-' + insight.status" x-text="insight.status"></span>
                                    <div class="flex space-x-1">
                                        <span x-show="insight.isDynamic" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Dynamic</span>
                                        <span x-show="insight.hasCta" class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">CTA</span>
                                    </div>
                                    <div class="text-xs text-gray-500">
                                        Priority: <span class="font-semibold" x-text="insight.priority"></span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Middle Column: Content -->
                            <div class="flex-1 min-w-0">
                                <h4 class="text-sm font-medium text-gray-700 mb-2">Content:</h4>
                                <p class="text-gray-600 text-sm leading-relaxed" x-text="insight.content"></p>
                                
                                <!-- Dynamic Variables -->
                                <div x-show="insight.templateKeys && insight.templateKeys.length > 0" class="mt-3">
                                    <h4 class="text-sm font-medium text-gray-700 mb-2">Dynamic Variables:</h4>
                                    <div class="flex flex-wrap gap-1">
                                        <template x-for="key in insight.templateKeys" :key="key">
                                            <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded" x-text="key"></span>
                                        </template>
                                    </div>
                                </div>
                                
                                <!-- CTA -->
                                <div x-show="insight.cta" class="mt-3">
                                    <h4 class="text-sm font-medium text-gray-700 mb-2">Call to Action:</h4>
                                    <div class="bg-gray-50 p-3 rounded">
                                        <div class="text-sm font-medium text-gray-900" x-text="insight.cta.text"></div>
                                        <div class="text-xs text-blue-600 mt-1 break-all" x-text="insight.cta.url"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Right Column: Requirements -->
                            <div class="flex-shrink-0 w-48">
                                <h4 class="text-sm font-medium text-gray-700 mb-2">Requirements:</h4>
                                <div class="text-xs text-gray-500 space-y-1">
                                    <div x-show="insight.requiresPrimaryUser" class="flex items-center">
                                        <svg class="w-3 h-3 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                        </svg>
                                        Primary User
                                    </div>
                                    <div x-show="insight.requiresProfileComplete" class="flex items-center">
                                        <svg class="w-3 h-3 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                        </svg>
                                        Profile Complete
                                    </div>
                                    <div x-show="insight.requiredContext && insight.requiredContext.length > 0" class="mt-2">
                                        <div class="text-xs font-medium text-gray-700">Context:</div>
                                        <div class="text-xs text-gray-600" x-text="insight.requiredContext.join(', ')"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>

            <!-- Empty State -->
            <div x-show="filteredInsights.length === 0" class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.709M15 6.291A7.962 7.962 0 0012 4c-2.34 0-4.29 1.009-5.824 2.709"></path>
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900">No insights found</h3>
                <p class="mt-1 text-sm text-gray-500">Try adjusting your search or filter criteria.</p>
            </div>
            </div>
        </div>
    </div>

    <script>
        function smartFactsDashboard() {{
            return {{
                searchQuery: '',
                statusFilter: '',
                typeFilter: '',
                viewMode: 'grid',
                
                insights: {insights_json},
                
                get filteredInsights() {{
                    return this.insights.filter(insight => {{
                        const matchesSearch = !this.searchQuery || 
                            insight.id.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            insight.content.toLowerCase().includes(this.searchQuery.toLowerCase());
                        
                        const matchesStatus = !this.statusFilter || insight.status === this.statusFilter;
                        
                        const matchesType = !this.typeFilter || 
                            (this.typeFilter === 'static' && !insight.isDynamic) ||
                            (this.typeFilter === 'dynamic' && insight.isDynamic);
                        
                        return matchesSearch && matchesStatus && matchesType;
                    }});
                }},
                
                get stats() {{
                    return {{
                        total: this.insights.length,
                        live: this.insights.filter(i => i.status === 'live').length,
                        review: this.insights.filter(i => i.status === 'review').length,
                        dynamic: this.insights.filter(i => i.isDynamic).length,
                        withCta: this.insights.filter(i => i.hasCta).length,
                        retired: this.insights.filter(i => i.status === 'retired').length
                    }};
                }},
                
                exportToCSV() {{
                    const csvData = this.filteredInsights.map(insight => ({{
                        'ID': insight.id,
                        'Status': insight.status,
                        'Priority': insight.priority,
                        'Type': insight.isDynamic ? 'Dynamic' : 'Static',
                        'Content': insight.content.replace(/\\n/g, ' ').replace(/\\r/g, ''),
                        'Dynamic Variables': insight.templateKeys ? insight.templateKeys.join('; ') : '',
                        'CTA Text': insight.cta ? insight.cta.text : '',
                        'CTA URL': insight.cta ? insight.cta.url : '',
                        'Required Context': insight.requiredContext ? insight.requiredContext.join('; ') : '',
                        'Requires Primary User': insight.requiresPrimaryUser ? 'Yes' : 'No',
                        'Requires Profile Complete': insight.requiresProfileComplete ? 'Yes' : 'No',
                        'Has CTA': insight.hasCta ? 'Yes' : 'No'
                    }}));
                    
                    // Convert to CSV
                    const headers = Object.keys(csvData[0]);
                    const csvContent = [
                        headers.join(','),
                        ...csvData.map(row => 
                            headers.map(header => {{
                                const value = row[header];
                                // Escape quotes and wrap in quotes if contains comma, quote, or newline
                                if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\\n'))) {{
                                    return `"${{value.replace(/"/g, '""')}}"`;
                                }}
                                return value;
                            }}).join(',')
                        )
                    ].join('\\n');
                    
                    // Create and download file
                    const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
                    const link = document.createElement('a');
                    const url = URL.createObjectURL(blob);
                    link.setAttribute('href', url);
                    link.setAttribute('download', `smart_facts_export_${{new Date().toISOString().split('T')[0]}}.csv`);
                    link.style.visibility = 'hidden';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }}
            }}
        }}
    </script>
</body>
</html>"""
    
    # Format the insights data as JSON
    insights_json = json.dumps(insights, indent=2)
    
    # Get current timestamp
    last_updated = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Replace placeholders in the template
    html_content = html_template.format(
        insights_json=insights_json,
        last_updated=last_updated
    )
    
    return html_content

def main():
    """Main function to build and deploy the dashboard"""
    print("Building Smart Facts Dashboard...")
    
    # Extract insights data
    insights = extract_smart_facts_from_codebase()
    print(f"Extracted {len(insights)} insights")
    
    # Generate HTML
    html_content = generate_dashboard_html(insights)
    
    # Write to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Dashboard built successfully!")
    print(f"Generated index.html with {len(insights)} insights")
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_content
    }

if __name__ == '__main__':
    main()
