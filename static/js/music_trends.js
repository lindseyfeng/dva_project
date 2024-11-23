let artistName;
document.addEventListener('DOMContentLoaded', () => {
    const trendsForm = document.getElementById('trends-form');
    const chartContainer = document.getElementById('chart-container');

    
    // Default chart data
    artistName = trendsForm.artist.value;
    const defaultTimePeriod = '3_months';
    const defaultData = generateDummyData(artistName, defaultTimePeriod);
    // Render the default chart
    renderLineChart(defaultData, defaultTimePeriod, artistName);

    trendsForm.onsubmit = (event) => {
        event.preventDefault();
        const artistSelect = trendsForm.artist;
        // const artist = artistSelect.options[artistSelect.selectedIndex].text;
        artistName = artistSelect.value;
        console.log(artistName)
        const timePeriod = trendsForm['time-period'].value;

        // Generate dummy data for the selected artist and time period
        const data = generateDummyData(artistName, timePeriod);

        // Clear previous chart (if any)
        chartContainer.innerHTML = '';

        // Render the line chart with the dummy data
        renderLineChart(data, timePeriod, artistName);
    };

    // window.addEventListener("resize", () => {
    //     const newWidth = document.getElementById("chart-container").clientWidth - margin.left - margin.right;
    //     const newHeight = document.getElementById("chart-container").clientHeight - margin.top - margin.bottom;
    
    //     d3.select("#chart-container svg")
    //       .attr("viewBox", `0 0 ${newWidth + margin.left + margin.right} ${newHeight + margin.top + margin.bottom}`);
    // });

    // Function to generate dummy data based on selected time period
    function generateDummyData(artist, timePeriod) {
        const data = [];
        let startDate;

        switch (timePeriod) {
            case '3_months':
                startDate = new Date();
                startDate.setMonth(startDate.getMonth() - 3);
                for (let i = 0; i <= 12; i++) {  // Weekly data for 3 months
                    const date = new Date(startDate);
                    date.setDate(startDate.getDate() + i * 7);
                    data.push({ date, popularity: Math.floor(Math.random() * 100) });
                }
                break;
            case '1_year':
                startDate = new Date();
                startDate.setFullYear(startDate.getFullYear() - 1);
                for (let i = 0; i <= 12; i++) {  // Monthly data for 1 year
                    const date = new Date(startDate);
                    date.setMonth(startDate.getMonth() + i);
                    data.push({ date, popularity: Math.floor(Math.random() * 100) });
                }
                break;
            case '5_years':
                startDate = new Date();
                startDate.setFullYear(startDate.getFullYear() - 5);
                for (let i = 0; i <= 20; i++) {  // Quarterly data for 5 years
                    const date = new Date(startDate);
                    date.setMonth(startDate.getMonth() + i * 3);
                    data.push({ date, popularity: Math.floor(Math.random() * 100) });
                }
                break;
            default:
                startDate = new Date();
                startDate.setFullYear(startDate.getFullYear() - 10);
                for (let i = 0; i <= 10; i++) {  // Yearly data for 10 years
                    const date = new Date(startDate);
                    date.setFullYear(startDate.getFullYear() + i);
                    data.push({ date, popularity: Math.floor(Math.random() * 100) });
                }
                break;
        }
        return data;
    }

    // Function to render the line chart with D3.js
    function renderLineChart(data, timePeriod) {
        console.log(artist);
        const margin = { top: 20, right: 30, bottom: 50, left: 50 };
        window.addEventListener("resize", () => {
            const newWidth = document.getElementById("chart-container").clientWidth - margin.left - margin.right;
            const newHeight = document.getElementById("chart-container").clientHeight - margin.top - margin.bottom;
        
            d3.select("#chart-container svg")
              .attr("viewBox", `0 0 ${newWidth + margin.left + margin.right} ${newHeight + margin.top + margin.bottom}`);
        });
        // Define the initial width and height based on the window size or container size
        const width = document.getElementById("chart-container").clientWidth - margin.left - margin.right;
        const height = document.getElementById("chart-container").clientHeight - margin.top - margin.bottom;

        const svg = d3.select("#chart-container")
                    .append("svg")
                    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                    .attr("preserveAspectRatio", "xMidYMid meet")  // Center alignment
                    .append("g")
                    .attr("transform", `translate(${margin.left},${margin.top})`);
    
        // const svg = d3.select("#chart-container")
        //               .append("svg")
        //               .attr("width", width + margin.left + margin.right)
        //               .attr("height", height + margin.top + margin.bottom)
        //               .append("g")
        //               .attr("transform", `translate(${margin.left},${margin.top})`);
    
        // X scale and axis
        const x = d3.scaleTime()
                    .domain(d3.extent(data, d => d.date))
                    .range([0, width]);
        svg.append("g")
           .attr("transform", `translate(0,${height})`)
           .call(d3.axisBottom(x).ticks(timePeriod === '3_months' ? d3.timeWeek : d3.timeYear))
           .attr("class", "x-axis");
    
        // Y scale and axis
        const y = d3.scaleLinear()
                    .domain([0, 100])
                    .range([height, 0]);
        // svg.append("g")
        //    .call(d3.axisLeft(y))
        //    .attr("class", "y-axis");
    
        // Define gradient
        const gradient = svg.append("defs")
                            .append("linearGradient")
                            .attr("id", "line-gradient")
                            .attr("x1", "0%")
                            .attr("y1", "0%")
                            .attr("x2", "0%")
                            .attr("y2", "100%");
        gradient.append("stop").attr("offset", "0%").attr("stop-color", "#007bff").attr("stop-opacity", 0.4);
        gradient.append("stop").attr("offset", "100%").attr("stop-color", "#007bff").attr("stop-opacity", 0);
    
        // Line generator
        const line = d3.line()
                       .x(d => x(d.date))
                       .y(d => y(d.popularity))
                       .curve(d3.curveMonotoneX);  // Smooth line
    
        // Area generator for gradient fill
        const area = d3.area()
                       .x(d => x(d.date))
                       .y0(height)
                       .y1(d => y(d.popularity))
                       .curve(d3.curveMonotoneX);
    
        // Append the area
        svg.append("path")
           .datum(data)
           .attr("fill", "url(#line-gradient)")
           .attr("d", area);
    
        // Append the line path with transition
        svg.append("path")
           .datum(data)
           .attr("fill", "none")
           .attr("stroke", "#007bff")
           .attr("stroke-width", 2)
           .attr("d", line)
           .attr("class", "line-path")
           .style("opacity", 0)
           .transition()
           .duration(1000)
           .style("opacity", 1);
    
        // Add data points with tooltips
        const tooltip = d3.select("#chart-container").append("div")
                          .attr("class", "tooltip")
                          .style("opacity", 0);
    
        svg.selectAll("circle")
           .data(data)
           .enter()
           .append("circle")
           .attr("cx", d => x(d.date))
           .attr("cy", d => y(d.popularity))
           .attr("r", 4)
           .attr("fill", "#007bff")
           .attr("class", "data-point")
           .on("mouseover", function(event, d) {
                d3.select(this).transition().attr("r", 6).attr("fill", "#0056b3");
                tooltip.transition().duration(200).style("opacity", 0.9);
                const mouseX = event.offsetX; // Get offset relative to SVG
                const mouseY = event.offsetY; // Get offset relative to SVG
                // Additional adjustments for tooltip positioning
                const tooltipWidth = tooltip.node().offsetWidth;
                const tooltipHeight = tooltip.node().offsetHeight;
                // Ensure tooltip stays within SVG bounds
                let left = mouseX; // Adjust horizontal offset
                let top = mouseY - 20; // Adjust vertical offset
                const svgWidth = svg.node().clientWidth;
                const svgHeight = svg.node().clientHeight;

                if (left + tooltipWidth > svgWidth) {
                left = svgWidth - tooltipWidth - 10; // Position to the left if needed
                }
                if (top - tooltipHeight < 0) {
                top = mouseY + 10; // Position below the circle if needed
                }

                tooltip.html(`<strong>Date:</strong> ${d.date.toLocaleDateString()}<br><strong>Popularity:</strong> ${d.popularity}`)
                    .style("left", `${left}px`)
                    .style("top", `${top}px`);
            })
        //         tooltip.html(`<strong>Date:</strong> ${d.date.toLocaleDateString()}<br><strong>Popularity:</strong> ${d.popularity}`)
        //                .style("left", (event.pageX) + "px")
        //                .style("top", (event.pageY) + "px");
        //    })
           .on("mouseout", function() {
                d3.select(this).transition().attr("r", 4).attr("fill", "#007bff");
                tooltip.transition().duration(500).style("opacity", 0);
           });
    
        // Add labels and title
        svg.append("text")
           .attr("x", width / 2)
           .attr("y", height + margin.bottom - 10)
           .attr("text-anchor", "middle")
           .attr("class", "x-label")
           .text("Date");
    
        // svg.append("text")
        //    .attr("transform", "rotate(-90)")
        //    .attr("x", -height / 2)
        //    .attr("y", -margin.left + 15)
        //    .attr("text-anchor", "middle")
        //    .attr("class", "y-label")
        //    .text("Popularity");
    
        svg.append("text")
           .attr("x", width / 2)
        //    .attr("y", -10)
           .attr("text-anchor", "middle")
           .attr("class", "chart-title")
           .text(`${artistName} Popularity Over Time`);
    }    
    

});
