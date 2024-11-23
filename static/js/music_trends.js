document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired'); // Debugging log
    const trendsForm = document.getElementById('trends-form');
    const chartContainer = document.getElementById('chart-container');

    if (!trendsForm) {
        console.error('Form element (#trends-form) not found in the DOM');
    }

    if (!chartContainer) {
        console.error('Chart container (#chart-container) not found in the DOM');
    }

    // Check if trendsData is available
    if (!trendsData || trendsData.length === 0) {
        console.error('trendsData is missing or empty', trendsData);
    } else {
        console.log('trendsData loaded successfully', trendsData);
    }

    // Default rendering
    let currentData = trendsData; // This is passed from Flask
    console.log('Initial data for chart:', currentData);

    if (currentData && currentData.length > 0) {
        renderLineChart(currentData, "Default Period", artistName);
    } else {
        console.warn('No data to render for the default chart.');
    }

    // Form submission event
    trendsForm.onsubmit = (event) => {
        event.preventDefault();
        console.log('Form submitted');
        
        const artistSelect = trendsForm.artist;
        if (!artistSelect) {
            console.error('Artist selection element not found');
            return;
        }

        artistName = artistSelect.value;
        console.log('Selected artist:', artistName);

        const timePeriod = trendsForm['time-period'].value;
        console.log('Selected time period:', timePeriod);

        // Filter or process the data based on user-selected time period
        const filteredData = filterDataByTimePeriod(currentData, timePeriod);
        console.log('Filtered data for the selected time period:', filteredData);

        // Clear previous chart
        chartContainer.innerHTML = '';
        console.log('Previous chart cleared');

        // Render the line chart with the filtered data
        if (filteredData && filteredData.length > 0) {
            renderLineChart(filteredData, timePeriod, artistName);
        } else {
            console.warn('No data to render after filtering.');
        }
    };

    // Filter data by time period
    function filterDataByTimePeriod(data, timePeriod) {
        console.log('Filtering data by time period:', timePeriod);
        const now = new Date();
        let startDate;

        switch (timePeriod) {
            case '3_months':
                startDate = new Date();
                startDate.setMonth(now.getMonth() - 3);
                break;
            case '1_year':
                startDate = new Date();
                startDate.setFullYear(now.getFullYear() - 1);
                break;
            default:
                startDate = new Date();
                startDate.setFullYear(now.getFullYear() - 10);
                break;
        }

        console.log('Calculated start date for filtering:', startDate);

        // Filter the data based on the calculated start date
        const filtered = data.filter(d => new Date(d.date) >= startDate);
        console.log('Filtered data:', filtered);
        return filtered;
    }

    // Render line chart
    function renderLineChart(data, timePeriod, artistName) {
        console.log('Rendering line chart with data:', data, 'for time period:', timePeriod);

        const margin = { top: 20, right: 30, bottom: 50, left: 50 };
        const width = document.getElementById("chart-container").clientWidth - margin.left - margin.right;
        const height = document.getElementById("chart-container").clientHeight - margin.top - margin.bottom;

        if (width <= 0 || height <= 0) {
            console.error('Chart container dimensions are invalid', { width, height });
            return;
        }

        console.log('Chart dimensions:', { width, height });

        const svg = d3.select("#chart-container")
                    .append("svg")
                    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                    .attr("preserveAspectRatio", "xMidYMid meet")
                    .append("g")
                    .attr("transform", `translate(${margin.left},${margin.top})`);

        // Scales and Axes
        const x = d3.scaleTime()
                    .domain(d3.extent(data, d => new Date(d.date)))
                    .range([0, width]);

        const y = d3.scaleLinear()
                    .domain([0, d3.max(data, d => d.metric)])
                    .range([height, 0]);

        svg.append("g")
           .attr("transform", `translate(0,${height})`)
           .call(d3.axisBottom(x));

        svg.append("g").call(d3.axisLeft(y));

        // Line
        const line = d3.line()
                       .x(d => x(new Date(d.date)))
                       .y(d => y(d.metric))
                       .curve(d3.curveMonotoneX);

        svg.append("path")
           .datum(data)
           .attr("fill", "none")
           .attr("stroke", "#007bff")
           .attr("stroke-width", 2)
           .attr("d", line);

        // Title
        svg.append("text")
           .attr("x", width / 2)
           .attr("y", -10)
           .attr("text-anchor", "middle")
           .text(`${artistName} Popularity Over Time`);

        console.log('Line chart rendered successfully');
    }
});
