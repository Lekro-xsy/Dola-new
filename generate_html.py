import json

# 读取data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 生成HTML模板
html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dola vs Normal 图像生成对比</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(45deg, #2c3e50, #34495e);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .controls {
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .nav-controls {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .nav-btn {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .nav-btn:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }

        .nav-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
        }

        .image-selector {
            padding: 8px 15px;
            border: 2px solid #007bff;
            border-radius: 25px;
            background: white;
            font-size: 16px;
            outline: none;
        }

        .current-info {
            font-weight: 500;
            color: #495057;
        }

        .comparison-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            min-height: 600px;
        }

        .image-panel {
            padding: 30px;
            position: relative;
        }

        .image-panel.normal {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            border-right: 2px solid #dee2e6;
        }

        .image-panel.dola {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }

        .panel-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .image-container {
            text-align: center;
            margin-bottom: 25px;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }

        .generated-image {
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }

        .generated-image:hover {
            transform: scale(1.02);
        }

        .image-placeholder {
            color: #6c757d;
            font-size: 1.1rem;
            text-align: center;
            padding: 20px;
        }

        .scores-container {
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }

        .score-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }

        .score-item:last-child {
            border-bottom: none;
            font-weight: bold;
            font-size: 1.1rem;
            color: #2c3e50;
        }

        .score-label {
            font-weight: 500;
            color: #495057;
        }

        .score-value {
            font-weight: 600;
            color: #007bff;
            font-size: 1.1rem;
        }

        .score-value.winner {
            color: #28a745;
            font-weight: bold;
        }

        .prompt-container {
            margin: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            color: white;
        }

        .prompt-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        }

        .prompt-text {
            font-size: 1rem;
            line-height: 1.6;
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        @media (max-width: 768px) {
            .comparison-container {
                grid-template-columns: 1fr;
            }
            
            .image-panel.normal {
                border-right: none;
                border-bottom: 2px solid #dee2e6;
            }
            
            .controls {
                flex-direction: column;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dola vs Normal 图像生成对比</h1>
            <p>侧重对比展示与评估分数</p>
        </div>

        <div class="controls">
            <div class="nav-controls">
                <button class="nav-btn" id="prevBtn" onclick="previousImage()">← 上一张</button>
                <button class="nav-btn" id="nextBtn" onclick="nextImage()">下一张 →</button>
                <select class="image-selector" id="imageSelector" onchange="goToImage()">
                    <!-- Options will be populated by JavaScript -->
                </select>
            </div>
            <div class="current-info">
                <span>第 <span id="currentIndex">1</span> 张，共 <span id="totalImages">100</span> 张</span>
            </div>
        </div>

        <div class="comparison-container">
            <div class="image-panel normal">
                <div class="panel-title">Normal 生成</div>
                <div class="image-container" id="normalImageContainer">
                    <div class="image-placeholder">加载中...</div>
                </div>
                <div class="scores-container">
                    <div class="score-item">
                        <span class="score-label">颜色分数:</span>
                        <span class="score-value" id="normalColorScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">空间分数:</span>
                        <span class="score-value" id="normalSpatialScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">计数分数:</span>
                        <span class="score-value" id="normalCountScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">相关性分数:</span>
                        <span class="score-value" id="normalRelevanceScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">总体分数:</span>
                        <span class="score-value" id="normalOverallScore">-</span>
                    </div>
                </div>
            </div>

            <div class="image-panel dola">
                <div class="panel-title">Dola 生成</div>
                <div class="image-container" id="dolaImageContainer">
                    <div class="image-placeholder">加载中...</div>
                </div>
                <div class="scores-container">
                    <div class="score-item">
                        <span class="score-label">颜色分数:</span>
                        <span class="score-value" id="dolaColorScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">空间分数:</span>
                        <span class="score-value" id="dolaSpatialScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">计数分数:</span>
                        <span class="score-value" id="dolaCountScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">相关性分数:</span>
                        <span class="score-value" id="dolaRelevanceScore">-</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">总体分数:</span>
                        <span class="score-value" id="dolaOverallScore">-</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="prompt-container">
            <div class="prompt-title">当前提示词</div>
            <div class="prompt-text" id="promptText">加载中...</div>
        </div>
    </div>

    <script>
        let currentImageIndex = 1;
        let totalImages = 100;
        
        // 嵌入数据
        const imageData = ''' + json.dumps(data, ensure_ascii=False, indent=2) + ''';

        function updateScoreDisplay(elementId, value, compareValue) {
            const element = document.getElementById(elementId);
            element.textContent = value.toFixed(3);
            
            // 如果这个分数更高，添加winner类
            if (value > compareValue && value > 0) {
                element.classList.add('winner');
            } else {
                element.classList.remove('winner');
            }
        }

        function updateDisplay() {
            const currentData = imageData[currentImageIndex.toString()];
            if (!currentData) {
                console.error('没有找到索引为', currentImageIndex, '的数据');
                return;
            }

            // 更新图片
            const normalImg = `Normal/prompt_${String(currentImageIndex).padStart(3, '0')}_normal.jpg`;
            const dolaImg = `Dola/prompt_${String(currentImageIndex).padStart(3, '0')}_standard_as_dola.jpg`;

            // 创建图片元素
            const normalContainer = document.getElementById('normalImageContainer');
            const dolaContainer = document.getElementById('dolaImageContainer');

            normalContainer.innerHTML = `<img class="generated-image" src="${normalImg}" alt="Normal generated image" onerror="this.parentElement.innerHTML='<div class=\\"image-placeholder\\">图片加载失败</div>'">`;
            dolaContainer.innerHTML = `<img class="generated-image" src="${dolaImg}" alt="Dola generated image" onerror="this.parentElement.innerHTML='<div class=\\"image-placeholder\\">图片加载失败</div>'">`;

            // 更新分数，并高亮显示更高的分数
            const normalScores = currentData.normal;
            const dolaScores = currentData.dola;

            updateScoreDisplay('normalColorScore', normalScores.color_score, dolaScores.color_score);
            updateScoreDisplay('dolaColorScore', dolaScores.color_score, normalScores.color_score);

            updateScoreDisplay('normalSpatialScore', normalScores.spatial_score, dolaScores.spatial_score);
            updateScoreDisplay('dolaSpatialScore', dolaScores.spatial_score, normalScores.spatial_score);

            updateScoreDisplay('normalCountScore', normalScores.count_score, dolaScores.count_score);
            updateScoreDisplay('dolaCountScore', dolaScores.count_score, normalScores.count_score);

            updateScoreDisplay('normalRelevanceScore', normalScores.relevance_score, dolaScores.relevance_score);
            updateScoreDisplay('dolaRelevanceScore', dolaScores.relevance_score, normalScores.relevance_score);

            updateScoreDisplay('normalOverallScore', normalScores.overall_score, dolaScores.overall_score);
            updateScoreDisplay('dolaOverallScore', dolaScores.overall_score, normalScores.overall_score);

            // 更新提示词
            document.getElementById('promptText').textContent = currentData.prompt || '暂无提示词';

            // 更新导航
            document.getElementById('currentIndex').textContent = currentImageIndex;
            document.getElementById('prevBtn').disabled = currentImageIndex === 1;
            document.getElementById('nextBtn').disabled = currentImageIndex === totalImages;
            document.getElementById('imageSelector').value = currentImageIndex;
        }

        function previousImage() {
            if (currentImageIndex > 1) {
                currentImageIndex--;
                updateDisplay();
            }
        }

        function nextImage() {
            if (currentImageIndex < totalImages) {
                currentImageIndex++;
                updateDisplay();
            }
        }

        function goToImage() {
            const selectedIndex = parseInt(document.getElementById('imageSelector').value);
            if (selectedIndex >= 1 && selectedIndex <= totalImages) {
                currentImageIndex = selectedIndex;
                updateDisplay();
            }
        }

        // 初始化选择器选项
        function initializeSelector() {
            const selector = document.getElementById('imageSelector');
            for (let i = 1; i <= totalImages; i++) {
                const option = document.createElement('option');
                option.value = i;
                option.textContent = `图片 ${i}`;
                selector.appendChild(option);
            }
        }

        // 键盘导航
        document.addEventListener('keydown', function(event) {
            if (event.key === 'ArrowLeft') {
                previousImage();
            } else if (event.key === 'ArrowRight') {
                nextImage();
            }
        });

        // 初始化页面
        document.addEventListener('DOMContentLoaded', function() {
            initializeSelector();
            updateDisplay();
        });
    </script>
</body>
</html>'''

# 写入文件
with open('comparison.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("已更新 comparison.html 文件，移除了详细错误信息")