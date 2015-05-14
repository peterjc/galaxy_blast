<!DOCTYPE HTML>
<html>
<head>

<!--

This BLAST visualization is part of the cross-bio project - Cross-filtered biological data.

http://crossb.io

Developed by Sebastian Wilzbach.

Source code
https://github.com/greenify/crossbio

Thanks Sebastian!

-->

    <title>${hda.name} | ${visualization_name}</title>
<%
    root = h.url_for( '/' )
%>

${h.stylesheet_link( root + 'plugins/visualizations/crossbio_blast/static/css/dc.css')}
${h.stylesheet_link( root + 'plugins/visualizations/crossbio_blast/static/css/bootstrap.css')}
${h.javascript_link( root + 'plugins/visualizations/crossbio_blast/static/js/crossbio.js' )}
${h.javascript_link( root + 'plugins/visualizations/crossbio_blast/static/js/biojsioblast.js' )}

</head>

## ----------------------------------------------------------------------------
<body>

<meta charset="utf8">

<div class="container">
    <div class="row">
        <div class="dc-data-count">
            <span class="filter-count"></span> selected out of <span class="total-count"></span> records
        </div>
    </div>

    <div class="row">

        <div id="blast-ident">
            <strong>Sequence identitiy</strong>
            <a class="reset" href="javascript:identChart.filterAll();dc.redrawAll();" style="display: none;">reset</a>
            <div class="clearfix"></div>
        </div>
        <div id="blast-length">
            <strong>Length distribution</strong>
            <a class="reset" href="javascript:lengthChart.filterAll();dc.redrawAll();" style="display: none;">reset</a>
            <div class="clearfix"></div>
        </div>
        <div id="blast-score">
            <strong>Score distribution</strong>
            <a class="reset" href="javascript:blastScore.filterAll();dc.redrawAll();" style="display: none;">reset</a>
            <div class="clearfix"></div>
        </div>

        <div id="blast-org">
            <strong>Organisms</strong>
            <a class="reset" href="javascript:blastOrg.filterAll();dc.redrawAll();" style="display: none;">reset</a>
            <div class="clearfix"></div>
        </div>

        <div id="blast-prot">
            <strong>Proteins</strong>
            <a class="reset" href="javascript:blastProt.filterAll();dc.redrawAll();" style="display: none;">reset</a>
            <div class="clearfix"></div>
        </div>

        <div class="row">
            <div id="blast-hssp">
                <strong>HSSP</strong>
                <a class="reset" href="javascript:blastHSSP.filterAll();dc.redrawAll();" style="display: none;">reset</a>
                <div class="clearfix"></div>
            </div>
        </div>

    </div>

    <!-- anchor div for data table -->
    <table class="dc-data-table table table-hover">
    </table>
</div>

    <script>
        /* global dc,crossfilter */ 
        require("crossbio");

        var lengthChart = dc.barChart('#blast-length');
        var identChart = dc.pieChart('#blast-ident');
        var blastScore = dc.rowChart('#blast-score');
        var blastProt = dc.pieChart('#blast-prot');
        var blastOrg= dc.pieChart('#blast-org');
        var blastHSSP = dc.scatterPlot('#blast-hssp');

        var Blast = require("biojs-io-blast");

        var url = "${root}api/histories/"+config.dataset_id+"/contents/" +config.dataset_id+ "/display";
        Blast.read(url, display);

        function display(err, result) {

          var hits = result.iterations[0].hits;

          var c = crossfilter(hits);
          var all = c.groupAll();

          var lengthDim = c.dimension(function(d) {
            return Math.round(d.len / 100) * 100;
          });
          var lengthGroup = lengthDim.group().reduceCount();

          var scoreDim = c.dimension(function(d) {
            return Math.round(parseInt(d.hsps[0].score) / 25) * 25;
          });
          var scoreGroup = scoreDim.group().reduceCount();

          var identDim = c.dimension(function(d) {
            var r = Math.round(parseInt(d.hsps[0].identity) / parseInt(d.hsps[0]["align-len"])  * 10) / 10;
            return r;
          });
          var identGroup = identDim.group().reduceCount();

          var protDim = c.dimension(function(d) {
            return d.def.split("|").pop().split(/[ ](.+)?/,2)[1].split(";")[0].split("=")[1];
          });
          var protGroup = protDim.group().reduceCount();

          var orgDim = c.dimension(function(d) {
            // uniprot specs are crazy
            var org = d.def.split("|").pop().split(/[ ](.+)?/,2)[1].split(";").pop();
            org = (/\[(.*)\]/).exec(org)[1];
            return org;
          });
          var orgGroup = orgDim.group().reduceCount();

          var hsspDim = c.dimension(function(d) {
            var alignLen = parseInt(d.hsps[0]["align-len"]);
            var seqIdent = parseInt(d.hsps[0].identity) / alignLen;
            return [alignLen, seqIdent];
          });
          var hsspGroup = hsspDim.group();

          blastHSSP.width(480)
            .height(200)
            .x(d3.scale.linear().domain([0,2000]))
            .y(d3.scale.linear().domain([0,0.5]))
            .elasticY(true)
            .yAxisLabel("Seq. identity")
            .xAxisLabel("Align length")
            .dimension(hsspDim)
            .group(hsspGroup);

          blastScore.width(180)
            .height(180)
            .dimension(scoreDim)
            .cap(10)
            .group(scoreGroup);

          identChart.width(180)
            .height(180)
            .radius(80)
            .innerRadius(30)
            .dimension(identDim)
            .group(identGroup);

          blastOrg.width(180)
            .height(180)
            .radius(80)
            .cap(10)
            .innerRadius(30)
            .dimension(orgDim)
            .group(orgGroup);

          blastProt.width(180)
            .height(180)
            .radius(80)
            .cap(10)
            .innerRadius(30)
            .dimension(protDim)
            .group(protGroup);

          lengthChart.width(400)
            .height(180)
            .x(d3.scale.linear().domain([-2500, 2500]))
            .elasticY(true)
            .elasticX(true)
            .dimension(lengthDim)
            .group(lengthGroup);

          var idDim = c.dimension(function(d) {
            return d.id;
          });

          dc.dataCount('.dc-data-count')
                .dimension(c)
                .group(all)
                .html({
                    some:'<strong>%filter-count</strong> selected out of <strong>%total-count</strong> records' +
                        ' | <a href=\'javascript:dc.filterAll(); dc.renderAll();\'\'>Reset All</a>',
                    all:'All records selected. Please click on the graph to apply filters.'
                });
           dc.dataTable('.dc-data-table')
                .dimension(idDim)
                .group(function(d){
                  return "BLAST results";
                })
                .size(10) // (optional) max number of records to be shown, :default = 25
                .columns([
                    'len',    // d['date'], ie, a field accessor; capitalized automatically
                    'id',    // ...
                    'def',   // ...
                    {
                        label: 'score', // desired format of column name 'Change' when used as a label with a function.
                        format: function (d) {
                            return d.hsps[0].score;
                        }
                    },
                    'accession'   // d['volume'], ie, a field accessor; capitalized automatically
                ])
                .sortBy(function (d) {
                    return parseInt(d.len);
                })
                .order(d3.ascending);

          dc.renderAll();
        }
    </script>

</body>
