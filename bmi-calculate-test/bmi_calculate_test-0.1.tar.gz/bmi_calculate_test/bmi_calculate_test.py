class Person:
    def __init__(self, name, weight, height):
        self.name = name
        self.weight = weight
        self.height = height

    def bmi(self):
        return self.weight / (self.height * self.height)

    def __str__(self):
        return f"{self.name} has a BMI of {self.bmi()}"

    def conclusion(self):
        if self.bmi() < 18.5:
            return "Underweight"
        elif self.bmi() < 25:
            return "Normal"
        elif self.bmi() < 30:
            return "Overweight"
        else:
            return "Obese"
