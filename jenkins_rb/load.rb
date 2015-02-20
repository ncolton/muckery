require 'rest_client'
require 'json'
require 'sparkr'
require 'term/ansicolor'
require 'yaml'

# The magic to make coloring work
class String
    include Term::ANSIColor
end

def load_config(configuration_file)
    fd = open configuration_file, 'r'
    configuration = YAML.load fd.read
    return configuration
end

def bucket_resize(data, items_per_bucket)
    buckets = []
    data.each_slice(items_per_bucket) do |batch|
        buckets << batch.inject(0) { |result, element| result + element }
    end
    return buckets
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

def build_query_url(config)
    if config[:ssl]
        scheme = 'https'
    else
        scheme = 'http'
    end

    "#{scheme}://#{config[:host]}#{config[:base_path]}#{config[:query_path]}?#{config[:query]}"
end

def write_output(data)
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
end

def parse_json_data(json_data)
    data = {
        'executors' => {
            'total' => {
                'hourly' => json_data['totalExecutors']['hour']['history'][0..23],
                '5min' => bucket_resize(json_data['totalExecutors']['min']['history'], 5)[0..11]
            },
            'busy' => {
                'hourly' => json_data['busyExecutors']['hour']['history'][0..23],
                '5min' => bucket_resize(json_data['busyExecutors']['min']['history'], 5)[0..11]
            }
        },
        'queue_length' => {
            'hourly' => json_data['totalQueueLength']['hour']['history'][0..23],
            '5min' => bucket_resize(json_data['totalQueueLength']['min']['history'], 5)[0..11]
        }
    }

    return data
end

def query_jenkins_for_stats(jenkins_configuration, auth_info)
    query_url = build_query_url jenkins_configuration

    plaintext_auth_string = "#{auth_info[:user]}:#{auth_info[:api_token]}"
    base64_auth_string = Base64.encode64 plaintext_auth_string
    base64_auth_string.chomp!

    stat_resource = RestClient::Resource.new query_url
    stats = JSON.parse(stat_resource.get)
    return stats
end


default_config_file = '.jenkins_load_config'
configuration = load_config default_config_file
stats = query_jenkins_for_stats configuration[:jenkins], configuration[:auth]
data = parse_json_data(stats)
write_output(data)
