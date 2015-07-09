moment.locale('nb');

var BookingListing = React.createClass({
    handleRemove: function(e) {
        this.props.onRemove(this.props.booking)
    },
    render: function() {
        var booking = this.props.booking;
        var tf = moment(booking.from_time).format("HH:mm");
        var tt = moment(booking.to_time).format("HH:mm");
        var owner = "";
        var removeButton = "";
        if (booking.type == 'member'){
            owner = (
                <p className="owner">
                      - <a href={"/medlemmer/" + booking.owner.id + "/"}>{booking.owner.name}</a>
                </p>
            );
            if (this.props.booking.owner.id == this.props.user){
                removeButton = (
                    <a href="#" title="Fjern booking" className="booking-remove" onClick={this.handleRemove}>
                        <span className="glyphicon glyphicon-remove"></span>
                    </a>
                );
            }
        }
        if (booking.type == 'global' && booking.owner){
            owner = (
                <p className="owner">- {booking.owner}</p>
            );
        }
        return(
            <div className={"booking " + booking.type + "Booking"}>
                <h4>{tf} - {tt} {removeButton}</h4>
                <p><span className="purpose">{booking.purpose}</span></p>
                {owner}
            </div>
        );
    }
});

var CalendarDay = React.createClass({
    handleRemoveClick: function(booking) {
        this.props.onBookingRemoved(booking)
    },
    render: function() {
        var user = this.props.user;
        var rc = this.handleRemoveClick;
        var bookings = this.props.bookings.map(function (booking) {
            return <BookingListing booking={booking} user={user} onRemove={rc} />
        });
        return(
            <div className="calendarDay">
                <div className="day-header">
                    <h3>{this.props.date.format('dddd DD.MM')}</h3>
                </div>
                <div className="day-body">
                    {bookings}
                </div>
            </div>

        );
    }
});

var WeekCalendar = React.createClass({
    changeWeeks: function (amount) {
        this.state.start.add(amount, 'weeks');
        this.updateEvents();
    },
    handleBookingRemoved: function(booking) {
        $.ajax({
            url: this.props.url + "/" + booking.id + "/",
            method: 'DELETE',
            success: function(data) {
                this.updateEvents();
            }.bind(this)
        });
    },
    nextWeek: function (e) {
        this.changeWeeks(1)
    },
    prevWeek: function (e) {
        this.changeWeeks(-1)
    },
    getInitialState: function () {
        return {data: [], start: moment().isoWeekday(1)};
    },
    groupData: function (data) {
        var groupedData = [[],[],[],[],[],[],[]];
        data.forEach(function(datum) {
            var ft = moment(datum.from_time);
            groupedData[ft.weekday()].push(datum)
        });
        return groupedData;
    },
    updateEvents: function () {
        $.ajax({
            url: this.props.url + '/?week=' + this.state.start.format("GGGG[W]WW"),
            dataType: 'json',
            cache: true,
            success: function (data) {
                this.setState({data: this.groupData(data)});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    componentDidMount: function () {
        this.updateEvents();
    },
    render: function () {
        var start = this.state.start;
        var user = this.props.user;
        var br = this.handleBookingRemoved;
        var days = this.state.data.map(function (bookings, index) {
            return (
                <CalendarDay bookings={bookings} key={index} date={start.clone().add(index,'days')}
                    user={user} onBookingRemoved={br} />
            );
        });
        return (
            <div className="panel panel-primary weekCalendar">
                <div className="panel-heading">
                    <h3 className="panel-title">
                        <a href="#" className="btn btn-primary btn-xs" onClick={this.prevWeek}>
                            <span className="glyphicon glyphicon-chevron-left"></span>
                        </a>
                    &nbsp;Uke {start.format("W, GGGG")}&nbsp;
                        <a href="#" className="btn btn-primary btn-xs" onClick={this.nextWeek}>
                            <span className="glyphicon glyphicon-chevron-right"></span>
                        </a> <a href="/ovingsspeil/ny_booking/" className="btn btn-primary btn-xs">
                            <span className="glyphicon glyphicon-plus"></span> Ny booking
                        </a>
                    </h3>
                </div>
                <div className="panel-body weeks">
                    {days}
                </div>
            </div>
        );
    }
});

React.render(
    <WeekCalendar url='/api/booking/bookings' user={1}/>,
    document.getElementById('calendar')
);