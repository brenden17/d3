## Install
* pip install -U flask
* pip install -U biopython

## d3.js
D3.js(Data-Driven Documents)는 웹브라우저에서 데이터를 효과적으로 표현할 수 있으며 사용자와 상호작용할 수 있도록 개발된 자바스크립트 라이브러리이다. 2011년부터 개발하여 2014년 4월에 3.4.6버전을 내놓았다.

개발자나 데이터 과학자들은 잘 정제된 결과 데이터나 실험하고 있지만 의미있는 데이터를 어떻게 잘 보여줄 수 있을까 많은 걱정을 해 왔다. 다양한 시각화 라이브러리가 있으나 값비싸거나 특수한 시스템에서만 작동하기 때문이다. D3.js는 열린 공간인 웹 환경에서 쉽고 다양하게 데이터를 표현할 수 있게하여 큰 호응을 얻고 있다.

지금부터 가벼운 예제로 D3.js를 사용해 보도록 하겠다. 다음과 같은 패키지를 설치해야 하나 클라이언트가 중심이 되기 때문에 원하지 않을 경우 설치하지 않아도 좋다. 서버측에서 두 서열을 비교하여 클라이언트에서 쉽게 표현될 수 있도록 데이터를 만든다. 보통 클라이언트에서 처리하는 형태는 다음과 같다.

> [{키:값}, {키:값}, {키:값}, {키:값}, {키:값}]

실제, 서열 ACCACTGATCGAAATTGTGGCCCGT와 서열 TTAGTAAGGCCAAACG을 비교하고 json형태로 만든다.
> 
    alignments = pairwise2.align.globalxx("ACCACTGATCGAAATTGTGGCCCGT",
                                            "TTAGTAAGGCCAAACG")
    data = [{'s':p[0],'d':p[1]} for p in zip(alignments[0][0], alignments[0][1])]
    return json.dumps(data)

키와값으로 구성되며 실제 서열은 다음과 같다. "d"는 비교 서열1, "s"는 비교 서열2를 나타낸다.

> [{"d": "T", "s": "A"}, {"d": "T", "s": "C"}, {"d": "-", "s": "C"}, {"d": "A", "s": "A"}, {"d": "-", "s": "C"}, {"d": "-", "s": "T"}, {"d": "G", "s": "G"}, {"d": "-", "s": "A"}, {"d": "T", "s": "T"}, {"d": "-", "s": "C"}, {"d": "-", "s": "G"}, {"d": "A", "s": "A"}, {"d": "-", "s": "A"}, {"d": "A", "s": "A"}, {"d": "-", "s": "T"}, {"d": "-", "s": "T"}, {"d": "G", "s": "G"}, {"d": "-", "s": "T"}, {"d": "G", "s": "G"}, {"d": "-", "s": "G"}, {"d": "C", "s": "C"}, {"d": "C", "s": "C"}, {"d": "A", "s": "-"}, {"d": "A", "s": "-"}, {"d": "A", "s": "-"}, {"d": "C", "s": "C"}, {"d": "G", "s": "G"}, {"d": "-", "s": "T"}]

이러한 데이터를 그리기 위해 먼저 그림판을 만들어야 한다. d3.js는 jquery와 마찬가지로 선택자(selector)를 사용하여 객체를 얻는다. <svg class="chart"></svg>를 객체를 얻은 후 연결문법(chain)을 사용하여 속성을 지정한다.

>
var svgWidth = 820, svgHeight = 220;
var svg = d3.select(".chart")
		        .attr("width", svgWidth)
	         	.attr("height", svgHeight);

그림판이 준비되었으니 그림판 위에 각 박스를 만들고 두 서열을 나타내 보자. 우선, 만들어진 데이터를 d3.json을 통해 가져온다. 

> d3.json("/alignment_json", function(error, data) {});

가져온 데이터는 두번째 매개변수에 정의된 함수로 처리된다. 데이터는 리스트 형태로 되어있기 때문에 하나 하나씩 처리하기 위해 
리스트의 forEach 메쏘드를 사용하여 처리한다.

> data.forEach(function (value, index, array) {});

value는 하나의 데이터가 되면 index는 순서를 나타낸다. 이전에 만든 svg에 "g" 태그를 추가하고 사각형을 만든다. 
	
>       svg.append("g")
	        .attr("transform", "translate(" + 20 * index + ", 0)").append("rect")
    		.attr("id", index.toString())
	        .attr("width", rectWidth)
	        .attr("height", rectHeight);

다음 해당하는 뉴클레오타이드 코드를 표시한다.

>	    svg.append("g")
	        .attr("transform", "translate(" + 20 * index + ", 0)").append("text")
		    .attr("x", 10)
		    .attr("y", 10)
	    	.attr("dy", ".35em")
		    .text(value.s); 

이와 같이 사각형을 그려주고 코드를 넣으주면 다음과 같은 모습이 된다.

기본적인 형태를 만들었다. 여기에 사용자와 상호 작용을 할 수 있도록 이벤트를 추가해 보도록 하자. 마우스를 올려 놓을 때 사각형의 색이 변경되며 해당하는 비교 서열의 뉴클레오타이드 코드도 변화하도록 한다. 간단히, 이전에 만든 사각형에 이벤트를 추가하면 된다.

>       svg.append("g")
	        .attr("transform", "translate(" + 20 * index + ", 0)").append("rect")
    		.attr("id", index.toString())
	        .attr("width", rectWidth)
	        .attr("height", rectHeight)
            .on("mouseover", function(){
			    d3.select(this)
                    .transition()
	    			.style("fill", "#ccc");
				
				var dIndex = d3.select(this).attr("id");
				d3.select("#dec" + dIndex)
				    .transition()
			    	.style("fill", "red");

			})
            .on("mouseout", function(){
				d3.select(this)
    				.transition()
    				.style("fill", "steelblue");
				
				var dIndex = d3.select(this).attr("id");
				d3.select("#dec" + dIndex)
				    .transition()
			    	.style("fill", "steelblue");
			});

on 메쏘드의 mouseover와 mouseout을 이벤트를 추가하였다.

대략 100 줄로 데이터를 쉽게 볼 수 있도록 하였다. 가장 기본적인 형태이지만 좀 더 그럴사한 시각화는 약간의 시간만 더 투자하면 된다.


## Reference
* http://d3js.org/
* http://bost.ocks.org/mike/bar/
* http://tutorials.jenkov.com/svg/index.html


