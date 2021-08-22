#include <stdio.h>
#include <string.h>

#include "hardware/adc.h"
#include "hardware/gpio.h"

#define ROLL_AVG_S 1024

int in_pin = 26;
int led_ctrl = 22;

int roll_avgs[ROLL_AVG_S];
int roll_avg = 0;
int roll_avg_i = 0;

int read();

int main()
{
    stdio_init_all();
    adc_gpio_init(in_pin);
    adc_init();
    adc_set_clkdiv(1);
    adc_select_input(in_pin - 26);

    gpio_init(led_ctrl);
    gpio_set_dir(led_ctrl, true);
    gpio_put(led_ctrl, 1);

    memset(roll_avgs, 0, ROLL_AVG_S);

    while (1)
    {
        int val = read();
        int old = roll_avgs[roll_avg_i];
        roll_avgs[roll_avg_i] = val;
        roll_avg += val - old;
        roll_avg_i++;
        if (roll_avg_i == ROLL_AVG_S)
            roll_avg_i = 0;
        printf("%d\n", roll_avg);
    }

    return 0;
}

int read()
{
    int sum = 0;
    for (int i = 0; i < 1024; i++)
    {
        gpio_put(led_ctrl, 1);
        int led_on = adc_read();
        gpio_put(led_ctrl, 0);
        sum += led_on - adc_read();
    }
    return sum << 10;
}