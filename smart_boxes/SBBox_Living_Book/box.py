"""
SBBox_Living_Book - Living Book Smart Box
Hiển thị Knowledge Graph tương tác với AI-Powered Analysis
Triết lý LIS: Tái sinh tri thức qua Ngữ pháp
"""

from typing import Dict, Any


class LivingBookBox:
    """
    Living Book Box - Knowledge Graph Visualization với AI Enhancement
    
    Tính năng:
    - Interactive Knowledge Graph (D3.js force-directed)
    - AI-Powered Analysis (Ollama Qwen2.5)
    - Real-time Stats Dashboard
    - Search & Filter
    - Atom Detail Modal
    - Batch AI Analysis
    """
    
    def render(self, config: Dict[str, Any] = None) -> str:
        return """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Living Book - AI Enhanced Knowledge Graph</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                /* Custom Styles */
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                }
                
                .atom-card {
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    cursor: pointer;
                    border-left: 4px solid transparent;
                }
                
                .atom-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                }
                
                .difficulty-beginner { border-left-color: #10B981; }
                .difficulty-intermediate { border-left-color: #F59E0B; }
                .difficulty-advanced { border-left-color: #EF4444; }
                .difficulty-unknown { border-left-color: #6B7280; }
                
                .analyzing {
                    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
                    opacity: 0.7;
                }
                
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
                
                .graph-node {
                    cursor: pointer;
                    transition: all 0.3s;
                }
                
                .graph-node:hover {
                    filter: brightness(1.2);
                }
                
                .stat-card {
                    transition: all 0.3s;
                }
                
                .stat-card:hover {
                    transform: translateY(-2px);
                }
                
                /* Scrollbar styling */
                ::-webkit-scrollbar {
                    width: 8px;
                    height: 8px;
                }
                
                ::-webkit-scrollbar-track {
                    background: #f1f5f9;
                    border-radius: 4px;
                }
                
                ::-webkit-scrollbar-thumb {
                    background: #cbd5e1;
                    border-radius: 4px;
                }
                
                ::-webkit-scrollbar-thumb:hover {
                    background: #94a3b8;
                }
                
                .line-clamp-2 {
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }
                
                .line-clamp-3 {
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }
            </style>
        </head>
        <body class="bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 min-h-screen p-6">
            <div class="max-w-7xl mx-auto">
                <!-- Header -->
                <div class="mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 class="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                            <span class="text-5xl"></span>
                            <span>Living Book</span>
                        </h1>
                        <p class="text-gray-600 text-lg">Knowledge Graph với AI-Powered Analysis</p>
                    </div>
                    <div class="flex gap-3">
                        <button onclick="analyzeAllAtoms()" 
                                class="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg shadow-lg hover:shadow-xl transition font-semibold flex items-center gap-2">
                            <span class="text-xl">✨</span>
                            <span>AI Analyze All</span>
                        </button>
                        <a href="/atom-manager" 
                           class="px-6 py-3 bg-white text-gray-700 rounded-lg shadow hover:shadow-md transition font-semibold flex items-center gap-2">
                            <span class="text-xl">🔧</span>
                            <span>Atom Manager</span>
                        </a>
                    </div>
                </div>

                <!-- Stats Bar -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div class="stat-card bg-white rounded-xl p-5 shadow-md border-l-4 border-blue-500">
                        <div class="text-3xl font-bold text-blue-600" id="totalAtoms">0</div>
                        <div class="text-sm text-gray-600 mt-1">Total Atoms</div>
                    </div>
                    <div class="stat-card bg-white rounded-xl p-5 shadow-md border-l-4 border-green-500">
                        <div class="text-3xl font-bold text-green-600" id="analyzedAtoms">0</div>
                        <div class="text-sm text-gray-600 mt-1">AI Analyzed</div>
                    </div>
                    <div class="stat-card bg-white rounded-xl p-5 shadow-md border-l-4 border-purple-500">
                        <div class="text-3xl font-bold text-purple-600" id="totalConcepts">0</div>
                        <div class="text-sm text-gray-600 mt-1">Concepts</div>
                    </div>
                    <div class="stat-card bg-white rounded-xl p-5 shadow-md border-l-4 border-orange-500">
                        <div class="text-3xl font-bold text-orange-600" id="totalRelations">0</div>
                        <div class="text-sm text-gray-600 mt-1">Relations</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <!-- Left: Knowledge Graph Visualization -->
                    <div class="lg:col-span-5 bg-white rounded-xl shadow-lg p-5">
                        <h2 class="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
                            <span class="text-2xl">🕸️</span>
                            <span>Knowledge Graph</span>
                        </h2>
                        <div id="graphContainer" class="h-[500px] border-2 border-gray-200 rounded-lg bg-gray-50 relative overflow-hidden">
                            <div id="graphLoading" class="hidden absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
                                <div class="text-center">
                                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-2"></div>
                                    <p class="text-gray-600">Loading graph...</p>
                                </div>
                            </div>
                            <div id="graphEmpty" class="absolute inset-0 flex items-center justify-center text-gray-400">
                                <div class="text-center">
                                    <div class="text-6xl mb-2"></div>
                                    <p>Knowledge Graph sẽ hiển thị ở đây</p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-3 flex flex-wrap gap-4 text-xs">
                            <div class="flex items-center gap-1">
                                <div class="w-3 h-3 rounded-full bg-green-500"></div>
                                <span>Beginner</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                                <span>Intermediate</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                                <span>Advanced</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <div class="w-3 h-3 rounded-full bg-gray-400"></div>
                                <span>Not Analyzed</span>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Atom List với AI Analysis -->
                    <div class="lg:col-span-7 space-y-4">
                        <div class="flex justify-between items-center">
                            <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                                <span class="text-2xl"></span>
                                <span>Knowledge Atoms</span>
                            </h2>
                            <input type="text" id="searchInput" placeholder="Search atoms..." 
                                   class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   oninput="filterAtoms()">
                        </div>
                        <div id="atomsList" class="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                            <!-- Atom cards sẽ render ở đây -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- Atom Detail Modal -->
            <div id="atomModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                <div class="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
                    <div class="p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 id="modalTitle" class="text-2xl font-bold text-gray-800"></h3>
                            <button onclick="closeModal()" class="text-gray-500 hover:text-gray-700 text-2xl font-bold">&times;</button>
                        </div>
                        <div id="modalContent"></div>
                    </div>
                </div>
            </div>

            <script>
                let atoms = [];
                let filteredAtoms = [];

                // Load atoms khi page load
                document.addEventListener('DOMContentLoaded', async () => {
                    await loadAtoms();
                });

                async function loadAtoms() {
                    try {
                        const response = await fetch('/api/atoms');
                        if (!response.ok) throw new Error('Failed to fetch atoms');
                        atoms = await response.json();
                        filteredAtoms = [...atoms];
                        renderAtoms();
                        renderGraph();
                        updateStats();
                    } catch (error) {
                        console.error('Error loading atoms:', error);
                        showNotification('Failed to load atoms', 'error');
                    }
                }

                function renderAtoms() {
                    const container = document.getElementById('atomsList');
                    container.innerHTML = '';

                    if (filteredAtoms.length === 0) {
                        container.innerHTML = '<div class="text-center text-gray-500 py-8"><div class="text-4xl mb-2">🔍</div><p>No atoms found</p></div>';
                        return;
                    }

                    filteredAtoms.forEach(atom => {
                        const analysis = atom.ai_analysis || {};
                        const difficulty = analysis.difficulty || 'unknown';
                        const isAnalyzed = !!atom.ai_analysis;
                        const concepts = analysis.concepts || [];
                        const keywords = analysis.keywords || [];
                        const summary = analysis.summary || '';
                        const atomId = atom.atom_id || atom.id;

                        const card = document.createElement('div');
                        card.className = `atom-card bg-white rounded-lg p-4 shadow-md difficulty-${difficulty}`;
                        
                        card.innerHTML = `
                            <div class="flex justify-between items-start mb-2">
                                <div class="flex-1">
                                    <h3 class="font-bold text-lg text-gray-800 mb-1">${atom.title || 'Untitled Atom'}</h3>
                                    <div class="flex items-center gap-2 text-xs text-gray-500 mb-2">
                                        <span>ID: ${atomId}</span>
                                        <span>•</span>
                                        <span class="capitalize px-2 py-0.5 rounded bg-gray-100">${atom.atom_type || 'concept'}</span>
                                    </div>
                                </div>
                                <div class="flex gap-2">
                                    ${!isAnalyzed ? `
                                        <button onclick="analyzeAtom('${atomId}')" 
                                                class="px-3 py-1.5 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 transition flex items-center gap-1">
                                            <span>✨</span>
                                            <span>Analyze</span>
                                        </button>
                                    ` : `
                                        <span class="px-3 py-1.5 bg-green-100 text-green-800 rounded text-sm font-medium">
                                            ✓ Analyzed
                                        </span>
                                    `}
                                    <button onclick="showAtomDetails('${atomId}')" 
                                            class="px-3 py-1.5 bg-blue-100 text-blue-800 rounded text-sm hover:bg-blue-200 transition">
                                        Details
                                    </button>
                                </div>
                            </div>
                            
                            <p class="text-gray-600 text-sm mb-3 line-clamp-2">${(atom.content || '').substring(0, 150)}...</p>
                            
                            ${isAnalyzed ? `
                                <div class="space-y-2 pt-2 border-t border-gray-100">
                                    ${keywords.length > 0 ? `
                                        <div class="flex gap-1.5 flex-wrap">
                                            ${keywords.slice(0, 5).map(k => `
                                                <span class="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-medium">${k}</span>
                                            `).join('')}
                                        </div>
                                    ` : ''}
                                    
                                    ${summary ? `
                                        <p class="text-sm text-gray-700 italic border-l-3 border-purple-400 pl-3 bg-purple-50 py-2 px-3 rounded">
                                            "${summary}"
                                        </p>
                                    ` : ''}
                                    
                                    <div class="flex flex-wrap gap-3 text-xs text-gray-600">
                                        <span class="flex items-center gap-1">
                                            📊 <strong class="capitalize">${difficulty}</strong>
                                        </span>
                                        <span class="flex items-center gap-1">
                                            🔗 ${(analysis.relations || []).length} relations
                                        </span>
                                        <span class="flex items-center gap-1">
                                            💡 ${concepts.length} concepts
                                        </span>
                                        ${(analysis.prerequisites || []).length > 0 ? `
                                            <span class="flex items-center gap-1">
                                                📚 ${analysis.prerequisites.length} prerequisites
                                            </span>
                                        ` : ''}
                                    </div>
                                </div>
                            ` : `
                                <div class="text-sm text-gray-500 italic bg-gray-50 py-2 px-3 rounded">
                                    💡 Click "Analyze" để AI phân tích nguyên tử này
                                </div>
                            `}
                        `;
                        
                        container.appendChild(card);
                    });
                }

                function renderGraph() {
                    const container = document.getElementById('graphContainer');
                    const loading = document.getElementById('graphLoading');
                    const empty = document.getElementById('graphEmpty');
                    
                    // Clear previous graph
                    const svg = container.querySelector('svg');
                    if (svg) svg.remove();
                    
                    if (atoms.length === 0) {
                        empty.classList.remove('hidden');
                        return;
                    }
                    
                    empty.classList.add('hidden');
                    loading.classList.remove('hidden');
                    
                    setTimeout(() => {
                        loading.classList.add('hidden');
                        
                        const width = container.clientWidth;
                        const height = 500;

                        const svg = d3.select('#graphContainer')
                            .append('svg')
                            .attr('width', '100%')
                            .attr('height', '100%')
                            .attr('viewBox', `0 0 ${width} ${height}`);

                        // Tạo nodes
                        const nodes = atoms.map(atom => {
                            const analysis = atom.ai_analysis || {};
                            const difficulty = analysis.difficulty || 'unknown';
                            const colors = {
                                'beginner': '#10B981',
                                'intermediate': '#F59E0B',
                                'advanced': '#EF4444',
                                'unknown': '#6B7280'
                            };
                            
                            return {
                                id: atom.atom_id || atom.id,
                                title: atom.title || 'Atom',
                                analyzed: !!atom.ai_analysis,
                                difficulty: difficulty,
                                color: colors[difficulty] || colors['unknown']
                            };
                        });

                        // Tạo links từ relations với validation
                        const links = [];
                        const existingNodeIds = new Set(nodes.map(n => n.id));
                        
                        atoms.forEach(atom => {
                            const relations = atom.ai_analysis?.relations || [];
                            relations.forEach(rel => {
                                // Chỉ tạo link nếu cả source và target đều tồn tại
                                if (existingNodeIds.has(rel.from) && existingNodeIds.has(rel.to)) {
                                    links.push({
                                        source: rel.from,
                                        target: rel.to,
                                        type: rel.type
                                    });
                                }
                            });
                        });

                        // Force simulation
                        const simulation = d3.forceSimulation(nodes)
                            .force('link', d3.forceLink(links).id(d => d.id).distance(120))
                            .force('charge', d3.forceManyBody().strength(-250))
                            .force('center', d3.forceCenter(width / 2, height / 2))
                            .force('collision', d3.forceCollide().radius(30));

                        // Vẽ links
                        const link = svg.append('g')
                            .selectAll('line')
                            .data(links)
                            .join('line')
                            .attr('stroke', '#CBD5E1')
                            .attr('stroke-width', 2)
                            .attr('stroke-opacity', 0.6);

                        // Vẽ nodes
                        const node = svg.append('g')
                            .selectAll('g')
                            .data(nodes)
                            .join('g')
                            .call(d3.drag()
                                .on('start', dragstarted)
                                .on('drag', dragged)
                                .on('end', dragended));

                        // Circle cho nodes
                        node.append('circle')
                            .attr('r', 18)
                            .attr('fill', d => d.color)
                            .attr('stroke', '#fff')
                            .attr('stroke-width', 2)
                            .classed('graph-node', true);

                        // Label cho nodes
                        node.append('text')
                            .text(d => d.title.length > 15 ? d.title.substring(0, 12) + '...' : d.title)
                            .attr('x', 22)
                            .attr('y', 5)
                            .attr('font-size', '11px')
                            .attr('fill', '#374151')
                            .attr('font-weight', '500');

                        // Tooltip
                        node.append('title')
                            .text(d => `${d.title}\\nDifficulty: ${d.difficulty}\\nAnalyzed: ${d.analyzed ? 'Yes' : 'No'}`);

                        // Update positions
                        simulation.on('tick', () => {
                            link
                                .attr('x1', d => d.source.x)
                                .attr('y1', d => d.source.y)
                                .attr('x2', d => d.target.x)
                                .attr('y2', d => d.target.y);

                            node
                                .attr('transform', d => `translate(${d.x},${d.y})`);
                        });

                        function dragstarted(event, d) {
                            if (!event.active) simulation.alphaTarget(0.3).restart();
                            d.fx = d.x;
                            d.fy = d.y;
                        }

                        function dragged(event, d) {
                            d.fx = event.x;
                            d.fy = event.y;
                        }

                        function dragended(event, d) {
                            if (!event.active) simulation.alphaTarget(0);
                            d.fx = null;
                            d.fy = null;
                        }
                    }, 100);
                }

                function updateStats() {
                    const total = atoms.length;
                    const analyzed = atoms.filter(a => a.ai_analysis).length;
                    const concepts = atoms.reduce((sum, a) => sum + (a.ai_analysis?.concepts?.length || 0), 0);
                    const relations = atoms.reduce((sum, a) => sum + (a.ai_analysis?.relations?.length || 0), 0);

                    animateNumber('totalAtoms', total);
                    animateNumber('analyzedAtoms', analyzed);
                    animateNumber('totalConcepts', concepts);
                    animateNumber('totalRelations', relations);
                }

                function animateNumber(elementId, target) {
                    const element = document.getElementById(elementId);
                    const duration = 1000;
                    const start = parseInt(element.textContent) || 0;
                    const startTime = performance.now();

                    function update(currentTime) {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
                        const current = Math.round(start + (target - start) * easeOutQuart);
                        
                        element.textContent = current;
                        
                        if (progress < 1) {
                            requestAnimationFrame(update);
                        }
                    }

                    requestAnimationFrame(update);
                }

                async function analyzeAtom(atomId) {
                    const card = event.target.closest('.atom-card');
                    const originalContent = card.innerHTML;
                    
                    card.classList.add('analyzing');
                    card.innerHTML = '<div class="flex items-center justify-center py-8"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mr-3"></div><span class="text-purple-600 font-medium">AI đang phân tích...</span></div>';
                    
                    try {
                        const response = await fetch(`/api/atoms/analyze?atom_id=${atomId}&provider=ollama`, {
                            method: 'POST'
                        });
                        
                        const result = await response.json();
                        
                        if (result.error) {
                            throw new Error(result.error);
                        }
                        
                        await loadAtoms();
                        showNotification('✅ Phân tích thành công!', 'success');
                    } catch (error) {
                        console.error('Error analyzing atom:', error);
                        card.innerHTML = originalContent;
                        showNotification('❌ Lỗi: ' + error.message, 'error');
                    } finally {
                        card.classList.remove('analyzing');
                    }
                }

                async function analyzeAllAtoms() {
                    if (!confirm('Phân tích tất cả atoms chưa được phân tích bằng AI?\\n\\nQuá trình này có thể mất vài phút tùy số lượng atoms.')) {
                        return;
                    }

                    const btn = event.target.closest('button');
                    const originalContent = btn.innerHTML;
                    btn.disabled = true;
                    btn.innerHTML = '<div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2 inline-block"></div>Analyzing...';
                    
                    try {
                        const response = await fetch('/api/atoms/batch-analyze?provider=ollama', {
                            method: 'POST'
                        });
                        
                        const result = await response.json();
                        
                        if (result.error) {
                            throw new Error(result.error);
                        }
                        
                        await loadAtoms();
                        showNotification(`✅ Đã phân tích ${result.analyzed_count} atoms!`, 'success');
                    } catch (error) {
                        console.error('Error batch analyzing:', error);
                        showNotification('❌ Lỗi: ' + error.message, 'error');
                    } finally {
                        btn.disabled = false;
                        btn.innerHTML = originalContent;
                    }
                }

                function showAtomDetails(atomId) {
                    const atom = atoms.find(a => (a.atom_id || a.id) === atomId);
                    if (!atom) return;

                    const analysis = atom.ai_analysis || {};
                    
                    document.getElementById('modalTitle').textContent = atom.title || 'Atom Details';
                    
                    let content = `
                        <div class="space-y-4">
                            <div>
                                <h4 class="font-semibold text-gray-700 mb-2"> Nội dung:</h4>
                                <div class="bg-gray-50 p-4 rounded-lg text-gray-700">${atom.content || 'No content'}</div>
                            </div>
                    `;
                    
                    if (analysis && Object.keys(analysis).length > 0 && !analysis.error) {
                        content += `
                            <div class="grid grid-cols-2 gap-4">
                                <div class="bg-blue-50 p-4 rounded-lg">
                                    <h4 class="font-semibold text-blue-800 mb-2"> Độ khó</h4>
                                    <p class="text-blue-900 capitalize font-medium">${analysis.difficulty || 'unknown'}</p>
                                </div>
                                <div class="bg-purple-50 p-4 rounded-lg">
                                    <h4 class="font-semibold text-purple-800 mb-2">🔗 Relations</h4>
                                    <p class="text-purple-900">${(analysis.relations || []).length}</p>
                                </div>
                            </div>
                            
                            ${analysis.summary ? `
                                <div>
                                    <h4 class="font-semibold text-gray-700 mb-2">📝 Tóm tắt:</h4>
                                    <p class="text-gray-700 italic bg-purple-50 p-3 rounded border-l-4 border-purple-400">"${analysis.summary}"</p>
                                </div>
                            ` : ''}
                            
                            ${(analysis.concepts || []).length > 0 ? `
                                <div>
                                    <h4 class="font-semibold text-gray-700 mb-2">💡 Concepts:</h4>
                                    <div class="flex flex-wrap gap-2">
                                        ${analysis.concepts.map(c => `<span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">${c}</span>`).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${(analysis.keywords || []).length > 0 ? `
                                <div>
                                    <h4 class="font-semibold text-gray-700 mb-2">🏷️ Keywords:</h4>
                                    <div class="flex flex-wrap gap-2">
                                        ${analysis.keywords.map(k => `<span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">${k}</span>`).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${(analysis.prerequisites || []).length > 0 ? `
                                <div>
                                    <h4 class="font-semibold text-gray-700 mb-2">📚 Prerequisites:</h4>
                                    <ul class="list-disc list-inside text-gray-700">
                                        ${analysis.prerequisites.map(p => `<li>${p}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${(analysis.relations || []).length > 0 ? `
                                <div>
                                    <h4 class="font-semibold text-gray-700 mb-2">🔗 Relations:</h4>
                                    <div class="space-y-2">
                                        ${analysis.relations.map(r => `
                                            <div class="bg-gray-50 p-2 rounded text-sm">
                                                <span class="font-medium">${r.from}</span>
                                                <span class="text-gray-500 mx-2">→</span>
                                                <span class="font-medium">${r.to}</span>
                                                <span class="text-xs text-gray-400 ml-2">(${r.type})</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        `;
                    } else {
                        content += `
                            <div class="text-center py-8 text-gray-500 bg-gray-50 rounded-lg">
                                <p class="text-lg mb-2">💡 Chưa được phân tích</p>
                                <button onclick="analyzeAtom('${atomId}'); closeModal();" 
                                        class="mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                                    Phân tích ngay
                                </button>
                            </div>
                        `;
                    }
                    
                    content += '</div>';
                    document.getElementById('modalContent').innerHTML = content;
                    document.getElementById('atomModal').classList.remove('hidden');
                }

                function closeModal() {
                    document.getElementById('atomModal').classList.add('hidden');
                }

                function filterAtoms() {
                    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                    filteredAtoms = atoms.filter(atom => 
                        (atom.title || '').toLowerCase().includes(searchTerm) ||
                        (atom.content || '').toLowerCase().includes(searchTerm) ||
                        (atom.ai_analysis?.keywords || []).some(k => k.toLowerCase().includes(searchTerm))
                    );
                    renderAtoms();
                }

                function showNotification(message, type = 'info') {
                    const div = document.createElement('div');
                    div.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 text-white font-medium transform transition-all duration-300 translate-x-full ${
                        type === 'success' ? 'bg-green-600' : 'bg-red-600'
                    }`;
                    div.textContent = message;
                    document.body.appendChild(div);
                    
                    setTimeout(() => div.classList.remove('translate-x-full'), 100);
                    setTimeout(() => {
                        div.classList.add('translate-x-full');
                        setTimeout(() => div.remove(), 300);
                    }, 3000);
                }

                // Close modal khi click outside
                document.getElementById('atomModal').addEventListener('click', function(e) {
                    if (e.target === this) {
                        closeModal();
                    }
                });
            </script>
        </body>
        </html>
        """