require 'rest_client'
require 'json'
require 'sparkr'
require 'term/ansicolor'

def bucket_resize(data, items_per_bucket)
    buckets = []
    data.each_slice(items_per_bucket) do |batch|
        buckets << batch.inject(0) { |result, element| result + element }
    end
    return buckets
end

# The magic to make coloring work
class String
    include Term::ANSIColor
end

def color_sparkline_by_value(data, yellow, red)
    sparkline = Sparkr.sparkline(data) do |tick, count, index|
        if count < yellow
            tick.color(:green)
        elsif count < red
            tick.color(:yellow)
        else
            tick.color(:red)
        end
    end
    return sparkline
end

# stat_resource = RestClient::Resource.new query_url, :user => auth[:user], :password => auth[:api_token]
stat_resource = RestClient::Resource.new query_url
stats = JSON.parse(stat_resource.get)

data = {
    'executors' => {
        'total' => {
            'hourly' => stats['totalExecutors']['hour']['history'][0..23],
            '5min' => bucket_resize(stats['totalExecutors']['min']['history'], 5)[0..11]
        },
        'busy' => {
            'hourly' => stats['busyExecutors']['hour']['history'][0..23],
            '5min' => bucket_resize(stats['busyExecutors']['min']['history'], 5)[0..11]
        }
    },
    'queue_length' => {
        'hourly' => stats['totalQueueLength']['hour']['history'][0..23],
        '5min' => bucket_resize(stats['totalQueueLength']['min']['history'], 5)[0..11]
    }
}

line_length = 50
puts ''
puts '      Executors'
puts ' Hourly    |     Total : ' + Sparkr.sparkline(data['executors']['total']['hourly'])
puts '           |      Busy : ' + Sparkr.sparkline(data['executors']['busy']['hourly'])
puts ' 5 minutes |     Total : ' + Sparkr.sparkline(data['executors']['total']['5min'])
puts '           |      Busy : ' + Sparkr.sparkline(data['executors']['busy']['5min'])
puts '=' * line_length
puts '    Queue  |    Hourly : ' + color_sparkline_by_value(data['queue_length']['hourly'], 5, 10)
puts '    Length | 5 minutes : ' + color_sparkline_by_value(data['queue_length']['5min'], 5, 10)
puts ''

# puts stats.keys
# busyExecutors
# queueLength
# totalExecutors
# totalQueueLength

