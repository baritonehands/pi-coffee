MstarCoffee = (function() {
    self = {};
    
    self.weight = ko.observable();
    self.percent = ko.observable();
    self.updated = ko.observable();
    
    var getStats = function() {
        $.getJSON('/stats', function(data) {
            self.weight(data.weight);
            self.percent(data.percent);
            self.updated(new Date());
        });
    };
    
    self.ctx = Raphael('coffee', 200, 400);

    self.liquid = self.ctx.rect(0, 0, 200, 400, 10);
    self.liquid.attr({fill: 'brown', stroke: 'transparent'});

    self.label = self.ctx.text(100, 20, '100%');
    self.label.attr({'font-size': '20px', fill: '#FFF'});
    
    self.urn = self.ctx.rect(0, 0, 200, 400, 10);

    self.percent.subscribe(function(percent) {
        var lAnim = Raphael.animation({height:(percent / 100) * 400, y: (1 - (percent / 100)) * 400}, 600, '<>');
        var txtAnim = Raphael.animation({y: (1 - (percent / 100)) * 400 + 20}, 600, '<>');
        self.liquid.animate(lAnim);
        self.label.animateWith(self.liquid, lAnim, txtAnim);
        self.label.attr({text: percent + '%'});
    });
    
    getStats();
    setInterval(getStats, 10000);
    
    return self;
}());

ko.applyBindings(MstarCoffee);
